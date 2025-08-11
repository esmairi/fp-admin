from fp_admin.apps.auth.models import (
    Group,
    GroupPermissionLink,
    Permission,
    User,
    UserGroupLink,
    UserPermissionLink,
)
from fp_admin.registry import AdminModel


class UserAdmin(AdminModel):
    model = User
    label = "Users"
    display_field = "username"


class GroupAdmin(AdminModel):
    model = Group
    label = "Groups"
    display_field = "name"


class PermissionAdmin(AdminModel):
    model = Permission
    label = "Permissions"


class GroupPermissionLinkdmin(AdminModel):
    model = GroupPermissionLink
    label = "GroupPermissionLink"


class UserPermissionLinkdmin(AdminModel):
    model = UserPermissionLink
    label = "GroupPermissionLink"


class UserGroupLinkdmin(AdminModel):
    model = UserGroupLink
    label = "UserGroupLink"
