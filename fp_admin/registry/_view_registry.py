from itertools import chain
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, cast

from sqlmodel import SQLModel

from fp_admin.models.views import BaseView, FormView, FormViewFactory, ListView

from ._base import BaseRegistry

if TYPE_CHECKING:
    from fp_admin.models.field import FieldError, FpField


class ViewNotFound(Exception):
    pass


class ViewRegistry(BaseRegistry[List[BaseView]]):

    def register(self, model: Type[SQLModel], view: BaseView) -> None:
        model_name = model.__name__.lower()
        if model_name not in self._registry:
            self._registry[model_name] = []
        self._registry[model_name].append(view)

    def find_by_name(self, view_name: str) -> BaseView | None:
        target_view = [
            v
            for v in chain.from_iterable(self._registry.values())
            if v.name == view_name
        ]
        if target_view:
            return target_view[0]
        return None

    def get_fields(
        self, model: str, view_type: Optional[str] = None
    ) -> List["FpField"]:
        views = self.get(model)
        if view_type and views:
            views = list(filter(lambda v: v.name == view_type, views))
        if not views:
            return []
        return [field for view in views for field in view.fields]

    def get_form_view(self, form_id: str) -> FormView:
        """Get form view configuration by form ID."""
        for _, views in self._registry.items():
            for view in views:
                if view.name == form_id and view.view_type == "form":
                    return cast("FormView", view)
        raise ViewNotFound(f"View not found: {form_id}")


view_registry = ViewRegistry()


class ViewBuilder(BaseView):

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        # If any key attribute is missing, call build()
        if not all(
            [
                getattr(cls, "name", None),
                getattr(cls, "fields", None),
            ]
        ):
            # to refactor
            instance = cls(name=cls.name, model=cls.model, view_type=cls.view_type)
            view = instance.build()
        else:
            # Construct the view from class attributes
            view = cls.create_from_attrs()

        # Validate field references before setting them
        cls._validate_field_references()

        # Set validate_form method on FormView if it exists in the builder
        if hasattr(cls, "validate_form") and view.view_type == "form":
            validate_method = getattr(cls, "validate_form")

            # Create a wrapper function to handle the method signature
            def validate_form_wrapper(form_data: Dict[str, Any]) -> List["FieldError"]:
                return validate_method(cls, form_data)  # type: ignore

            # Use setattr to bypass type checking
            setattr(view, "validate_form", validate_form_wrapper)

        # Set creation_fields if it exists in the builder
        if hasattr(cls, "creation_fields") and cls.creation_fields:
            setattr(view, "creation_fields", cls.creation_fields)

        # Set allowed_update_fields if it exists in the builder
        if hasattr(cls, "allowed_update_fields") and cls.allowed_update_fields:
            setattr(view, "allowed_update_fields", cls.allowed_update_fields)

        # Set display_fields if it exists in the builder
        if hasattr(cls, "display_fields") and cls.display_fields:
            setattr(view, "display_fields", cls.display_fields)

        view_registry.register(cls.model, view)

    @classmethod
    def _validate_field_references(cls) -> None:
        """Validate that fields referenced in creation_fields and
         allowed_update_fields exist in the fields list.

        Raises:
            ValueError: If any referenced fields don't exist in the fields list
        """
        if not hasattr(cls, "fields") or not cls.fields:
            return  # No fields defined, skip validation

        # Get the set of field names that exist in the fields list
        existing_field_names = {field.name for field in cls.fields}

        # Validate creation_fields + allowed_update_fields + display_fields
        fields = []
        if hasattr(cls, "creation_fields") and cls.creation_fields:
            fields.extend(cls.creation_fields)
        if hasattr(cls, "allowed_update_fields") and cls.allowed_update_fields:
            fields.extend(cls.allowed_update_fields)
        if hasattr(cls, "display_fields") and cls.display_fields:
            fields.extend(cls.display_fields)

        missing_creation_fields = [
            name for name in fields if name not in existing_field_names
        ]
        if missing_creation_fields:
            raise ValueError(
                f"model: # {cls.__name__} # "
                f"Fields referenced fields do not exist in the "
                "view's fields: " + f"{missing_creation_fields}"
            )

    def build(self) -> FormView | ListView:
        if self.view_type == "form":
            return FormViewFactory(self.model).build_view()
        if self.view_type == "list":
            # For list views, we need to determine the default_form_id
            default_form_id = self._get_default_form_id()
            # Create a custom ListView with the determined default_form_id
            return ListView(
                name=f"{self.model.__name__}List",
                view_type="list",
                model=self.model,
                default_form_id=default_form_id,
                fields=FormViewFactory(self.model).get_fields(),
            )
        raise ValueError(f"Unknown view type: {self.view_type}")

    @classmethod
    def create_from_attrs(cls) -> FormView | ListView:
        if cls.view_type == "form":
            return FormView(
                name=cls.name,
                view_type="form",
                model=cls.model,
                fields=cls.fields or [],
            )
        if cls.view_type == "list":
            # For list views, determine the default_form_id
            default_form_id = cls._get_default_form_id()
            return ListView(
                name=cls.name,
                view_type="list",
                model=cls.model,
                default_form_id=default_form_id,
                fields=cls.fields or [],
            )
        raise ValueError(f"Unknown view type: {cls.view_type}")

    @classmethod
    def _get_default_form_id(cls) -> str | None:
        """Get the default form ID for list views.

        If default_form_id is explicitly set, use it.
        Otherwise, find the first form view for this model.
        If no form view exists, use a default naming convention.
        """
        # If explicitly set, use it
        if cls.default_form_id:
            return cls.default_form_id

        # Find the first form view for this model
        model_name = cls.model.__name__.lower()
        registered_views = view_registry.get(model_name)

        if registered_views:
            # Look for the first form view
            for view in registered_views:
                if view.view_type == "form":
                    return view.name

        # Fallback to default naming convention
        return f"{cls.model.__name__}Form"
