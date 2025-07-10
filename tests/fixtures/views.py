from fp_admin.admin.fields import FieldFactory
from fp_admin.admin.models import AdminModel
from fp_admin.admin.views import BaseViewBuilder
from tests.fixtures.models import ModelTest


class ModelTestAdmin(AdminModel):
    model = ModelTest
    label = "Test Model"


class ModelTestFormView(BaseViewBuilder):
    model = ModelTest
    view_type = "form"
    name = "test_form"
    fields = [
        FieldFactory.primarykey_field(name="id", title="ID"),
        FieldFactory.text_field(name="name", title="Name", required=True),
        FieldFactory.text_field(name="description", title="Description", required=True),
    ]
    creation_fields = ["name", "description"]
    allowed_update_fields = ["name", "description"]


class ModelTestListView(BaseViewBuilder):
    model = ModelTest
    view_type = "list"
    name = "test_list"
    fields = [
        FieldFactory.primarykey_field(name="id", title="ID"),
        FieldFactory.text_field(name="name", title="Name"),
        FieldFactory.text_field(name="description", title="Description"),
    ]
