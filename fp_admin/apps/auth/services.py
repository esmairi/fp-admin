from typing import Any, Dict, Optional, cast

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlmodel import Session

from fp_admin.providers.internal import InternalProvider, TokenResponse
from fp_admin.services.base import BaseService
from fp_admin.services.create_service import CreateRecordParams, CreateService
from fp_admin.settings_loader import settings

from ...providers.exceptions import AuthError
from .models import User
from .schemas import (
    SignupRequestData,
    SignupResponse,
    UserResponse,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: Session):
        self.create_service = CreateService(session)
        self.base_service = BaseService(session)

    def create_user(self, data: SignupRequestData) -> SignupResponse:
        data.password = pwd_context.hash(data.password)
        params = CreateRecordParams(data=data.model_dump(), form_id="UserForm")
        user_dict = self.create_service.create_record("user", params)
        user_response = UserResponse(**user_dict)
        return SignupResponse(data=user_response, message="USER CREATED")

    def get_user_by_username(self, username: str) -> Optional[User]:
        users = self.base_service.filter(User, username=username)
        return User(**users[0]) if users else None

    def serialize_user(self, user: User) -> Dict[str, Any]:
        return self.base_service.serialize(user, include_relationships=True)

    async def authenticate_and_issue_token(
        self, username: str, password: str
    ) -> TokenResponse[UserResponse]:
        provider = self.get_internal_provider()
        token_data = await provider.authenticate_and_issue_token(username, password)
        if not token_data:
            raise HTTPException(status_code=401, detail="INVALID CREDENTIALS")
        return token_data

    async def refresh_token(self, username: str, refresh_token: str) -> Any:
        provider = self.get_internal_provider()
        user = self.get_user_by_username(username)
        if not user:
            raise AuthError()
        return await provider.refresh_token(refresh_token, cast(UserResponse, user))

    async def user_auth_func(
        self, username: str, password: str
    ) -> Optional[Dict[str, Any]]:
        user = self.base_service.filter(User, username=username)
        if user and pwd_context.verify(password, user[0]["password"]):
            return user[0]
        return None

    def get_internal_provider(self) -> InternalProvider[UserResponse]:
        return InternalProvider[UserResponse](
            secret_key=settings.SECRET_KEY,
            access_token_expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_token_expires_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
            user_auth_func=self.user_auth_func,
        )
