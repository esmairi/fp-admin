from fp_admin.admin.views.base import BaseViewFactory
from fp_admin.admin.views.types import FormView, ListView


class FormViewFactory(BaseViewFactory):
    def build_view(self) -> FormView:
        return FormView(
            name=f"{self.model.__name__}Form",
            model=self.model.__name__.lower(),
            fields=self.get_fields(),
        )


class ListViewFactory(BaseViewFactory):
    def build_view(self) -> ListView:
        return ListView(
            name=f"{self.model.__name__}List",
            model=self.model.__name__.lower(),
            default_form_id=f"{self.model.__name__}Form",
            fields=self.get_fields(),
        )
