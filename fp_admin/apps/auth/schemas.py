from datetime import datetime
from typing import List, Literal, Optional, TypedDict

from pydantic import BaseModel, EmailStr

from fp_admin.apps.auth.models import GenderEnum
from fp_admin.providers.internal import TokenResponse


class GroupResponse(BaseModel):
    id: int
    name: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: GenderEnum
    is_active: bool
    is_superuser: bool
    is_deleted: bool
    email_verified: bool
    last_login: Optional[datetime] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    groups: List[GroupResponse] = []


class SignupRequestData(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[GenderEnum] = GenderEnum.PREFER_NOT_TO_SAY


class SignupRequest(BaseModel):
    data: SignupRequestData


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    errors: List[ErrorDetail]
    message: Optional[str] = None


class SignupResponse(BaseModel):
    data: UserResponse
    message: str


class SigninRequestData(BaseModel):
    username: str
    password: str
    remember_me: bool = False


class SigninRequest(BaseModel):
    data: SigninRequestData


class JWTPayload(TypedDict):
    sub: str
    exp: int  # UNIX timestamp
    type: Literal["access", "refresh"]


class RefreshRequest(BaseModel):
    refresh_token: str
    username: str


class SigninResponse(BaseModel):
    data: TokenResponse[UserResponse]
