from fp_admin.admin.models import AdminModel
from fp_admin.apps.auth.models import (
    Group,
    GroupPermissionLink,
    Permission,
    User,
    UserGroupLink,
)


class UserAdmin(AdminModel):
    model = User
    label = "Users"


class GroupAdmin(AdminModel):
    model = Group
    label = "Groups"


class PermissionAdmin(AdminModel):
    model = Permission
    label = "Permissions"


class GroupPermissionLinkdmin(AdminModel):
    model = GroupPermissionLink
    label = "GroupPermissionLink"


class UserGroupLinkdmin(AdminModel):
    model = UserGroupLink
    label = "UserGroupLink"
