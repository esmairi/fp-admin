from typing import Any, Dict, List, Literal, Optional, Type

from sqlmodel import SQLModel

from fp_admin.admin.fields import FieldError, FieldView
from fp_admin.admin.views.factories import FormViewFactory
from fp_admin.admin.views.registry import view_registry
from fp_admin.admin.views.views_types import BaseView, FormView, ListView


class BaseViewBuilder:
    name: str
    model: Type[SQLModel]
    view_type: Literal["form", "list"]
    fields: List[FieldView]
    default_form_id: Optional[str] = None
    creation_fields: Optional[List[str]] = None
    allowed_update_fields: Optional[List[str]] = None

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        # If any key attribute is missing, call build()
        if not all(
            [
                getattr(cls, "name", None),
                getattr(cls, "fields", None),
            ]
        ):
            instance = cls()
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
            def validate_form_wrapper(form_data: Dict[str, Any]) -> List[FieldError]:
                return validate_method(cls(), form_data)  # type: ignore

            # Use setattr to bypass type checking
            setattr(view, "validate_form", validate_form_wrapper)

        # Set creation_fields if it exists in the builder
        if hasattr(cls, "creation_fields") and cls.creation_fields:
            setattr(view, "creation_fields", cls.creation_fields)

        # Set allowed_update_fields if it exists in the builder
        if hasattr(cls, "allowed_update_fields") and cls.allowed_update_fields:
            setattr(view, "allowed_update_fields", cls.allowed_update_fields)

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

        # Validate creation_fields
        if hasattr(cls, "creation_fields") and cls.creation_fields:
            missing_creation_fields = [
                name for name in cls.creation_fields if name not in existing_field_names
            ]
            if missing_creation_fields:
                raise ValueError(
                    "Fields referenced in creation_fields do not exist in the "
                    "view's fields: " + f"{missing_creation_fields}"
                )

        # Validate allowed_update_fields
        if hasattr(cls, "allowed_update_fields") and cls.allowed_update_fields:
            missing_update_fields = [
                name
                for name in cls.allowed_update_fields
                if name not in existing_field_names
            ]
            if missing_update_fields:
                raise ValueError(
                    "Fields referenced in allowed_update_fields do not exist in the "
                    "view's fields: "
                    f"{missing_update_fields}"
                )

    def build(self) -> BaseView:
        if self.view_type == "form":
            return FormViewFactory(self.model).build_view()
        if self.view_type == "list":
            # For list views, we need to determine the default_form_id
            default_form_id = self._get_default_form_id()
            # Create a custom ListView with the determined default_form_id
            return ListView(
                name=f"{self.model.__name__}List",
                view_type="list",
                model=self.model.__name__.lower(),
                default_form_id=default_form_id,
                fields=FormViewFactory(self.model).get_fields(),
            )
        raise ValueError(f"Unknown view type: {self.view_type}")

    @classmethod
    def create_from_attrs(cls) -> BaseView:
        if cls.view_type == "form":
            return FormView(
                name=cls.name,
                view_type="form",
                model=cls.model.__name__.lower(),
                fields=cls.fields or [],
            )
        if cls.view_type == "list":
            # For list views, determine the default_form_id
            default_form_id = cls._get_default_form_id()
            return ListView(
                name=cls.name,
                view_type="list",
                model=cls.model.__name__.lower(),
                default_form_id=default_form_id,
                fields=cls.fields or [],
            )
        raise ValueError(f"Unknown view type: {cls.view_type}")

    @classmethod
    def _get_default_form_id(cls) -> str:
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
