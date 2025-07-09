from fp_admin.admin.fields import FieldView
from fp_admin.admin.views import BaseViewBuilder
from fp_admin.apps.auth.models import Group, User


class UserFormView(BaseViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"
    fields = [
        FieldView(
            name="id",
            field_type="number",
            is_primary_key=True,
            disabled=True,
            readonly=True,
        ),
        FieldView(name="username", title="Username", field_type="text"),
        FieldView(name="email", title="Email", field_type="text"),
        FieldView(name="is_active", title="Is Active", field_type="checkbox"),
    ]


class UserListView(BaseViewBuilder):
    model = User
    view_type = "list"
    name = "UserList"


class GroupListView(BaseViewBuilder):
    model = Group
    view_type = "list"
    name = "GroupList"


class GroupFormView(BaseViewBuilder):
    model = Group
    view_type = "form"
    name = "GroupForm"
