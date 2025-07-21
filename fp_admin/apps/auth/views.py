from fp_admin.admin.fields import FieldFactory
from fp_admin.admin.views import BaseViewBuilder
from fp_admin.apps.auth.models import Group, Permission, User


class UserFormView(BaseViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("username", "Username", required=True),
        FieldFactory.email_field("email", "Email", required=True),
        FieldFactory.password_field(
            "password", "Password", required=True, min_length=8
        ),
        FieldFactory.string_field("first_name", "First Name"),
        FieldFactory.string_field("last_name", "Last Name"),
        FieldFactory.choice_field(
            "gender",
            "Gender",
            options={
                "choices": [
                    ("male", "Male"),
                    ("female", "Female"),
                    ("non-binary", "Non-binary"),
                    ("other", "Other"),
                    ("prefer_not_to_say", "Prefer not to say"),
                ]
            },
        ),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),
        FieldFactory.boolean_field("is_deleted", "Deleted"),
        FieldFactory.boolean_field("email_verified", "Email Verified"),
        FieldFactory.datetime_field("last_login", "Last Login"),
        FieldFactory.string_field("avatar_url", "Avatar URL"),
        FieldFactory.string_field("bio", "Bio"),
        FieldFactory.many_to_many_field(
            "groups", "Groups", model_class=Group, field_title="name"
        ),
        FieldFactory.datetime_field("created_at", "Created At"),
        FieldFactory.datetime_field("updated_at", "Updated At"),
    ]

    creation_fields = [
        "username",
        "email",
        "password",
        "first_name",
        "last_name",
        "gender",
        "is_active",
        "is_superuser",
        "is_deleted",
        "email_verified",
        "avatar_url",
        "bio",
    ]
    allowed_update_fields = [
        "email",
        "first_name",
        "last_name",
        "gender",
        "is_active",
        "is_superuser",
        "is_deleted",
        "email_verified",
        "avatar_url",
        "bio",
    ]


class UserListView(BaseViewBuilder):
    model = User
    view_type = "list"
    name = "UserList"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("username", "Username"),
        FieldFactory.email_field("email", "Email"),
        FieldFactory.string_field("first_name", "First Name"),
        FieldFactory.string_field("last_name", "Last Name"),
        FieldFactory.choice_field(
            "gender",
            "Gender",
            options={
                "choices": [
                    ("male", "Male"),
                    ("female", "Female"),
                    ("non-binary", "Non-binary"),
                    ("other", "Other"),
                    ("prefer_not_to_say", "Prefer not to say"),
                ]
            },
        ),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),
        FieldFactory.boolean_field("is_deleted", "Deleted"),
        FieldFactory.boolean_field("email_verified", "Email Verified"),
        FieldFactory.datetime_field("last_login", "Last Login"),
        FieldFactory.string_field("avatar_url", "Avatar URL"),
        FieldFactory.string_field("bio", "Bio"),
        FieldFactory.datetime_field("created_at", "Created At"),
        FieldFactory.datetime_field("updated_at", "Updated At"),
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
