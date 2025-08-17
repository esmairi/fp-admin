from fp_admin.registry import ViewBuilder
from fp_admin.models.field import FieldFactory


# class MyModelFormView(ViewBuilder):
#     model = MyModel
#     view_type = "form"
#     name = "MyModelForm"
#     fields = [
#         FieldFactory.string_field("username", title="Username", required=True),
#         FieldFactory.string_field("first_name", title="Username", required=True),
#     ]
#     creation_fields = ["username", "first_name"]
#     allowed_update_fields = ["first_name"]
#
#
# class MyModelListView(ViewBuilder):
#     model = MyModel
#     view_type = "list"
#     name = "MyModelList"
