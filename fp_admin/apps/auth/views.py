from fp_admin.admin.fields import FieldFactory
from fp_admin.admin.views import BaseViewBuilder
from fp_admin.apps.auth.models import Group, Permission, User


class UserFormView(BaseViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field(
            "username",
            "Username",
            required=True,
        ),
        FieldFactory.email_field("email", "Email", required=True),
        FieldFactory.password_field(
            "password", "Password", required=True, min_length=8
        ),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),
        FieldFactory.many_to_many_field(
            "groups", "Groups", model_class=Group, field_title="name"
        ),
    ]

    creation_fields = ["username", "email", "password", "is_active", "is_superuser"]
    allowed_update_fields = ["email", "is_active", "is_superuser"]


class UserListView(BaseViewBuilder):
    model = User
    view_type = "list"
    name = "UserList"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("username", "Username"),
        FieldFactory.email_field("email", "Email"),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),
    ]


class GroupListView(BaseViewBuilder):
    model = Group
    view_type = "list"
    name = "GroupList"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("name", "Name"),
        FieldFactory.string_field("description", "Description"),
    ]


class GroupFormView(BaseViewBuilder):
    model = Group
    view_type = "form"
    name = "GroupForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("name", "Name", required=True, min_length=1),
        FieldFactory.string_field(
            "description", "Description", required=True, min_length=1, max_length=200
        ),
        FieldFactory.many_to_many_field(
            "permissions", "Permissions", model_class=Permission, field_title="name"
        ),
        FieldFactory.many_to_many_field(
            "users", "Users", model_class=User, field_title="username"
        ),
    ]

    creation_fields = ["name", "description"]
    allowed_update_fields = ["name", "description", "permissions"]


class PermissionListView(BaseViewBuilder):
    model = Permission
    view_type = "list"
    name = "PermissionList"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("codename", "Code Name"),
        FieldFactory.string_field("name", "Name"),
        FieldFactory.string_field("description", "Description"),
    ]


class PermissionFormView(BaseViewBuilder):
    model = Permission
    view_type = "form"
    name = "PermissionForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field(
            "codename", "Code Name", required=True, min_length=1, max_length=150
        ),
        FieldFactory.string_field(
            "name", "Name", required=True, min_length=1, max_length=150
        ),
        FieldFactory.string_field(
            "description", "Description", required=True, min_length=1, max_length=200
        ),
        FieldFactory.many_to_many_field(
            "groups", "Groups", model_class=Group, field_title="name"
        ),
    ]

    creation_fields = ["codename", "name", "description"]
    allowed_update_fields = ["codename", "name", "description"]
