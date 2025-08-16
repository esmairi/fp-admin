from datetime import UTC, datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class TimestampedModel(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )


class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    PREFER_NOT_TO_SAY = "PREFER_NOT_TO_SAY"


class UserGroupLink(SQLModel, table=True, tablename="user_group_link"):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    group_id: int = Field(foreign_key="group.id", primary_key=True)


class GroupPermissionLink(SQLModel, table=True, table_name="group_permission"):
    group_id: int = Field(foreign_key="group.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)


class UserPermissionLink(SQLModel, table=True, table_name="user_permission"):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)


class Permission(TimestampedModel, SQLModel, table=True, table_name="permission"):
    id: Optional[int] = Field(default=None, primary_key=True)
    codename: str = Field(nullable=False, unique=True, max_length=150)
    name: str = Field(nullable=False, max_length=150)
    description: str = Field(title="Description", max_length=200)
    groups: List["Group"] = Relationship(
        back_populates="permissions",
        link_model=GroupPermissionLink,
    )
    users: List["User"] = Relationship(
        back_populates="permissions", link_model=UserPermissionLink
    )


class Group(TimestampedModel, SQLModel, table=True, table_name="group"):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, max_length=150)
    description: str = Field(title="Description", max_length=200)

    permissions: List[Permission] = Relationship(
        back_populates="groups", link_model=GroupPermissionLink
    )
    users: List["User"] = Relationship(
        back_populates="groups", link_model=UserGroupLink
    )


class User(TimestampedModel, SQLModel, table=True, table_name="user"):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(title="Username", nullable=False, unique=True, max_length=150)
    email: str = Field(
        title="Email",
        nullable=False,
        unique=True,
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        max_length=255,
    )
    password: str = Field(title="Password", nullable=False)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    gender: GenderEnum = Field(default=GenderEnum.PREFER_NOT_TO_SAY, max_length=32)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)
    is_deleted: bool = Field(default=False, nullable=False)
    email_verified: bool = Field(default=False, nullable=False)
    last_login: Optional[datetime] = Field(default=None)
    avatar_url: Optional[str] = Field(default=None, max_length=512)
    bio: Optional[str] = Field(default=None, max_length=500)

    groups: List[Group] = Relationship(back_populates="users", link_model=UserGroupLink)
    permissions: List[Permission] = Relationship(
        back_populates="users", link_model=UserPermissionLink
    )
    oauth_accounts: List["UserOAuthAccount"] = Relationship(back_populates="user")


class UserOAuthAccount(
    TimestampedModel, SQLModel, table=True, table_name="user_oauth_account"
):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    provider: str = Field(nullable=False, max_length=50)
    provider_user_id: str = Field(nullable=False, max_length=255)
    user: Optional[User] = Relationship(back_populates="oauth_accounts")


User.model_rebuild()
Group.model_rebuild()
Permission.model_rebuild()
