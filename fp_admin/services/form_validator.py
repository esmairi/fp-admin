"""
Form validation service for fp-admin.

This module provides validation logic based on form configurations.
"""

from typing import Any, Dict, List, Optional

from fp_admin.admin.fields.errors import FieldError, get_error_message
from fp_admin.admin.views import view_registry
from fp_admin.admin.views.views_types import BaseView


class FormValidator:
    """Validates form data based on form configurations."""

    @classmethod
    def validate_form_data(
        cls, form_id: str, data: Dict[str, Any]
    ) -> Dict[str, List[FieldError]]:
        """
        Validate form data based on form configuration.

        Args:
            form_id: The form ID to get validation rules from
            data: The data to validate

        Returns:
            Dictionary mapping field names to lists of FieldError objects
        """
        field_errors: Dict[str, List[FieldError]] = {}

        # Step 1: Get FormView from view_registry
        form_view = cls._get_form_view(form_id)
        if not form_view:
            field_errors["_general"] = [
                FieldError(
                    code="NOT_FOUND",
                    message=get_error_message("NOT_FOUND", form_id=form_id),
                )
            ]
            return field_errors

        # Step 2: Get fields from the FormView
        fields = form_view.fields

        # Step 3: For each field, apply the existing validator
        for field in fields:
            field_name = field.name
            field_value = data.get(field_name)

            # Use the existing FieldView.validate_value method
            errors = field.validate_value(field_value)
            if errors:
                field_errors[field_name] = errors

        # Step 4: Apply custom form validation if no field errors
        if not field_errors:
            custom_errors = cls._apply_custom_form_validation(form_view, data)
            if custom_errors:
                field_errors["_form"] = custom_errors

        return field_errors

    @classmethod
    def _get_form_view(cls, form_id: str) -> Optional[BaseView]:
        """Get form view configuration by form ID."""
        all_views = view_registry.all()
        for _, views in all_views.items():
            for view in views:
                if view.name == form_id and view.view_type == "form":
                    return view
        return None

    @classmethod
    def _apply_custom_form_validation(
        cls, form_view: BaseView, data: Dict[str, Any]
    ) -> List[FieldError]:
        """
        Apply custom form validation if the form view has a validate_form method.

        Args:
            form_view: The form view
            data: The form data

        Returns:
            List of FieldError objects from custom validation
        """
        # Check if the form view has a validate_form method
        validate_method = getattr(form_view, "validate_form", None)
        if validate_method:
            return validate_method(data)  # type: ignore
        return []

    @classmethod
    def validate_and_raise(cls, form_id: str, data: Dict[str, Any]) -> None:
        """
        Validate form data and raise ValidationError if validation fails.

        Args:
            form_id: The form ID to get validation rules from
            data: The data to validate

        Raises:
            ValidationError: If validation fails
        """
        field_errors = cls.validate_form_data(form_id, data)

        if field_errors:
            from fp_admin.exceptions import ValidationError

            raise ValidationError(
                f"Validation failed for form '{form_id}'",
                details={"field_errors": field_errors},
            )
