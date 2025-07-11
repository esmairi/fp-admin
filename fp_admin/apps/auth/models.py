from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class UserGroupLink(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    group_id: int = Field(foreign_key="group.id", primary_key=True)


class GroupPermissionLink(SQLModel, table=True):
    group_id: int = Field(foreign_key="group.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)


class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codename: str
    name: str

    groups: List["Group"] = Relationship(
        back_populates="permissions", link_model=GroupPermissionLink
    )


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    permissions: List[Permission] = Relationship(
        back_populates="groups", link_model=GroupPermissionLink
    )
    users: List["User"] = Relationship(
        back_populates="groups", link_model=UserGroupLink
    )


class User(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False

    groups: List[Group] = Relationship(back_populates="users", link_model=UserGroupLink)
