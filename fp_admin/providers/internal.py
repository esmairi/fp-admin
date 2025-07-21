from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, Generic, Optional, TypeVar, cast

import jwt  # PyJWT
from fastapi import HTTPException, status
from pydantic import BaseModel

from . import OAuth2Provider
from .exceptions import AuthError

T = TypeVar("T")


class TokenResponse(BaseModel, Generic[T]):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: T


class InternalProvider(OAuth2Provider, Generic[T]):

    def __init__(
        self,
        secret_key: str,
        access_token_expires_minutes: int,
        refresh_token_expires_minutes: int,
        algorithm: str = "HS256",
        user_auth_func: Optional[Callable[[str, str], Any]] = None,
    ):  # pylint: disable=R0913,R0917
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expires_minutes = access_token_expires_minutes
        self.refresh_token_expires_minutes = refresh_token_expires_minutes
        self.user_auth_func = (
            user_auth_func  # function: (username, password) -> user dict or None
        )

    @property
    def name(self) -> str:
        return "internal"

    def get_authorize_url(self, state: str) -> str:
        # Not used for internal provider
        return ""

    async def get_access_token(self, code: str) -> Dict[str, Any]:
        # Not used for internal provider
        return {}

    async def get_user_info(self, token: Dict[str, Any]) -> Dict[str, Any]:
        # Decode JWT and return user info
        try:
            payload = jwt.decode(
                token["access_token"], self.secret_key, algorithms=[self.algorithm]
            )
            return {"sub": payload.get("sub"), "exp": payload.get("exp")}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID TOKEN"
            ) from e

    def __issue_token(self, user: Dict[str, Any]) -> TokenResponse[T]:
        now = datetime.now(timezone.utc)
        access_exp = now + timedelta(minutes=self.access_token_expires_minutes)
        refresh_exp = now + timedelta(minutes=self.refresh_token_expires_minutes)
        user_info = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
        }
        access_token = jwt.encode(
            {"sub": user_info, "exp": access_exp.timestamp(), "type": "access"},
            self.secret_key,
            algorithm=self.algorithm,
        )

        refresh_token = jwt.encode(
            {"sub": user_info, "exp": refresh_exp.timestamp(), "type": "refresh"},
            self.secret_key,
            algorithm=self.algorithm,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=cast(T, user),
        )

    async def authenticate_and_issue_token(
        self, username: str, password: str
    ) -> TokenResponse[T]:
        if not self.user_auth_func:
            raise RuntimeError("user_auth_func must be provided")

        user = await self.user_auth_func(username, password)
        if not user:
            raise AuthError()
        return self.__issue_token(user)

    def decode_token(self, token: str) -> Any:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    def refresh_token(self, refresh_token: str, user: T) -> TokenResponse[T]:
        try:
            payload = self.decode_token(refresh_token)
            if payload.get("type") != "refresh":  # check username
                raise AuthError()
        except Exception as e:
            raise AuthError() from e

        return self.__issue_token(user)  # type: ignore
