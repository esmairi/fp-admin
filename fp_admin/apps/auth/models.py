from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class UserGroupLink(SQLModel, table=True, tablename="user_group_link"):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    group_id: int = Field(foreign_key="group.id", primary_key=True)


class GroupPermissionLink(SQLModel, table=True, table_name="group_permission"):
    group_id: int = Field(foreign_key="group.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)


class Permission(SQLModel, table=True, table_name="permission"):
    id: Optional[int] = Field(default=None, primary_key=True)
    codename: str = Field(nullable=False, unique=True, max_length=150)
    name: str = Field(nullable=False, max_length=150)
    description: str = Field(title="Description", max_length=200)
    groups: List["Group"] = Relationship(
        back_populates="permissions", link_model=GroupPermissionLink
    )


class Group(SQLModel, table=True, table_name="group"):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, max_length=150)
    description: str = Field(title="Description", max_length=200)

    permissions: List[Permission] = Relationship(
        back_populates="groups", link_model=GroupPermissionLink
    )
    users: List["User"] = Relationship(
        back_populates="groups", link_model=UserGroupLink
    )


class User(SQLModel, table=True, table_name="user"):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(title="Username", nullable=False, unique=True, max_length=150)
    email: str = Field(
        title="Email",
        nullable=False,
        unique=True,
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    )
    password: str = Field(title="Password", nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)

    groups: List[Group] = Relationship(back_populates="users", link_model=UserGroupLink)


User.model_rebuild()
Group.model_rebuild()
Permission.model_rebuild()
