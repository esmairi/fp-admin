from fp_admin.apps.auth.models import Group, Permission, User
from fp_admin.models.field import FieldFactory, FpFieldError, FpFieldValidator
from fp_admin.registry import ViewBuilder


class UserFormView(ViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field("username", title="Username", required=True),
        FieldFactory.email_field("email", title="Email", required=True),
        FieldFactory.password_field(
            "password",
            title="Password",
            required=True,
            validators=[
                FpFieldValidator(
                    name="min_length",
                    condition_value=8,
                    error=FpFieldError(code="too_short", message="Too short"),
                )
            ],
        ),
        FieldFactory.string_field("first_name", title="First Name"),
        FieldFactory.string_field("last_name", title="Last Name"),
        FieldFactory.choice_field(
            "gender",
            title="Gender",
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
        FieldFactory.boolean_field("is_active", title="Active"),
        FieldFactory.boolean_field("is_superuser", title="Superuser"),
        FieldFactory.boolean_field("is_deleted", title="Deleted"),
        FieldFactory.boolean_field("email_verified", title="Email Verified"),
        FieldFactory.datetime_field("last_login", title="Last Login"),
        FieldFactory.string_field("avatar_url", title="Avatar URL"),
        FieldFactory.string_field("bio", title="Bio"),
        FieldFactory.many_to_many_field(
            "groups", title="Groups", model_class=Group, display_field="name"
        ),
        FieldFactory.datetime_field("created_at", title="Created At"),
        FieldFactory.datetime_field("updated_at", title="Updated At"),
    ]

    display_fields = [
        "username",
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
        "groups",
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
        "groups",
    ]


class UserListView(ViewBuilder):
    model = User
    view_type = "list"
    name = "UserList"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field("username", title="Username"),
        FieldFactory.email_field("email", title="Email"),
        FieldFactory.string_field("first_name", title="First Name"),
        FieldFactory.string_field("last_name", title="Last Name"),
        FieldFactory.choice_field(
            "gender",
            title="Gender",
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
        FieldFactory.boolean_field("is_active", title="Active"),
        FieldFactory.boolean_field("is_superuser", title="Superuser"),
        FieldFactory.boolean_field("is_deleted", title="Deleted"),
        FieldFactory.boolean_field("email_verified", title="Email Verified"),
        FieldFactory.datetime_field("last_login", title="Last Login"),
        FieldFactory.string_field("avatar_url", title="Avatar URL"),
        FieldFactory.string_field("bio", title="Bio"),
        FieldFactory.datetime_field("created_at", title="Created At"),
        FieldFactory.datetime_field("updated_at", title="Updated At"),
    ]


class GroupListView(ViewBuilder):
    model = Group
    view_type = "list"
    name = "GroupList"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field("name", title="Name"),
        FieldFactory.string_field("description", title="Description"),
    ]


class GroupFormView(ViewBuilder):
    model = Group
    view_type = "form"
    name = "GroupForm"

    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field("name", title="Name", required=True, min_length=1),
        FieldFactory.string_field(
            "description",
            title="Description",
            required=True,
            min_length=1,
            max_length=200,
        ),
        FieldFactory.many_to_many_field(
            "permissions",
            title="Permissions",
            model_class=Permission,
            display_field="name",
        ),
        FieldFactory.many_to_many_field(
            "users", title="Users", model_class=User, display_field="username"
        ),
    ]

    display_fields = ["name", "description", "users"]
    creation_fields = ["name", "description", "users", "permissions"]
    allowed_update_fields = ["name", "description", "permissions", "users"]


class PermissionListView(ViewBuilder):
    model = Permission
    view_type = "list"
    name = "PermissionList"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field("codename", title="Code Name"),
        FieldFactory.string_field("name", title="Name"),
        FieldFactory.string_field("description", title="Description"),
    ]


class PermissionFormView(ViewBuilder):
    model = Permission
    view_type = "form"
    name = "PermissionForm"

    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field(
            "codename", title="Code Name", required=True, min_length=1, max_length=150
        ),
        FieldFactory.string_field(
            "name", title="Name", required=True, min_length=1, max_length=150
        ),
        FieldFactory.string_field(
            "description",
            title="Description",
            required=True,
            min_length=1,
            max_length=200,
        ),
        FieldFactory.many_to_many_field(
            "groups", title="Groups", model_class=Group, display_field="name"
        ),
    ]

    display_fields = ["codename", "name", "description"]
    creation_fields = ["codename", "name", "description"]
    allowed_update_fields = ["codename", "name", "description"]
