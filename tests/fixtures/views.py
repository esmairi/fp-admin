from fp_admin.models.field import FieldFactory
from fp_admin.registry import AdminModel, ViewBuilder
from tests.fixtures.models import ModelTest


class ModelTestAdmin(AdminModel):
    model = ModelTest
    label = "Test Model"


class ModelTestFormView(ViewBuilder):
    model = ModelTest
    view_type = "form"
    name = "test_form"
    fields = [
        FieldFactory.primary_key_field(name="id", title="ID"),
        FieldFactory.text_field(name="name", title="Name", required=True),
        FieldFactory.text_field(name="description", title="Description", required=True),
    ]
    creation_fields = ["name", "description"]
    allowed_update_fields = ["name", "description"]


class ModelTestListView(ViewBuilder):
    model = ModelTest
    view_type = "list"
    name = "test_list"
    fields = [
        FieldFactory.primary_key_field(name="id", title="ID"),
        FieldFactory.text_field(name="name", title="Name"),
        FieldFactory.text_field(name="description", title="Description"),
    ]
