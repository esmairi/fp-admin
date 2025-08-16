from typing import Any, Dict, Optional

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fp_admin.providers.exceptions import AuthError
from fp_admin.providers.internal import InternalProvider, TokenResponse
from fp_admin.schemas import CreateRecordParams
from fp_admin.services.v1 import CreateService
from fp_admin.settings_loader import settings

from .models import User
from .schemas import (
    SignupRequestData,
    SignupResponse,
    UserResponse,
)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserService:
    def __init__(self, session: AsyncSession):
        self.create_service = CreateService(User, "user")
        self.session = session

    async def create_user(self, data: SignupRequestData) -> SignupResponse:
        stmt = select(User).where(User.username == data.username)
        exists = await self.session.exec(stmt)
        if exists.first():
            raise ValueError("User already exists")
        data.password = pwd_context.hash(data.password)
        params = CreateRecordParams(data=data.model_dump(), form_id="UserForm")
        user_dict: Dict[str, Any] = await self.create_service.create_record(
            self.session, params, True
        )  # type: ignore
        user_response = UserResponse(**user_dict)
        return SignupResponse(data=user_response, message="USER CREATED")

    async def get_user_by_username(self, username: str) -> Optional[User]:
        users = await self.create_service.filter(self.session, username=username)
        return User(**users[0]) if users else None

    def serialize_user(self, user: User) -> Dict[str, Any]:
        return user.model_dump()

    async def authenticate_and_issue_token(
        self, username: str, password: str
    ) -> TokenResponse[UserResponse]:
        provider = self.get_internal_provider()
        token_data = await provider.authenticate_and_issue_token(username, password)
        if not token_data:
            raise HTTPException(status_code=401, detail="INVALID CREDENTIALS")
        return token_data

    async def refresh_token(self, refresh_token: str, username: str) -> Any:
        provider = self.get_internal_provider()
        user = await self.get_user_by_username(username)
        if not user:
            raise AuthError()
        return provider.refresh_token(refresh_token, user.model_dump())

    async def user_auth_func(
        self, username: str, password: str
    ) -> Optional[Dict[str, Any]]:
        user = await self.create_service.filter(self.session, username=username)
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
