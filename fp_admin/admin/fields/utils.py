"""
Field utilities for fp-admin.

This module provides utility functions for working with fields and SQLModel conversion.
"""

import sys
from typing import Any, List, Literal, cast, get_args, get_origin, get_type_hints

from sqlmodel import SQLModel

from .base import FieldView
from .field_factory import FieldFactory
from .field_validator import FieldValidation
from .types import FieldType


def sqlmodel_to_fieldviews(model: type[SQLModel]) -> List[FieldView]:
    """
    Convert a SQLModel class to a list of FieldView objects.

    Args:
        model: SQLModel class to convert

    Returns:
        List of FieldView objects representing the model's fields

    Example:
        >>> from sqlmodel import SQLModel, Field
        >>> from typing import Literal
        >>>
        >>> class User(SQLModel):
        ...     id: int = Field(primary_key=True)
        ...     name: str = Field(max_length=100)
        ...     status: Literal["active", "inactive"] = Field(default="active")
        >>>
        >>> fields = sqlmodel_to_fieldviews(User)
        >>> for field in fields:
        ...     print(f"{field.name}: {field.field_type}")
    """
    field_views = []
    type_hints = get_type_hints(model)

    for field_name, field_info in model.model_fields.items():
        # Skip internal SQLModel fields
        if field_name in ["__class__", "__dict__", "__weakref__"]:
            continue

        # Get field type and metadata
        field_type = type_hints.get(field_name, Any)

        # Check for primary key fields
        is_primary_key = getattr(field_info, "primary_key", False) is True

        # Determine field type based on Python type
        field_type_str = _get_field_type(field_type)

        # Create validation rules
        validation = _create_validation(field_info)

        # Create FieldView using appropriate factory method
        if is_primary_key:
            field_view = FieldFactory.primarykey_field(
                field_name, _format_field_title(field_name)
            )
        elif field_type_str == "string":
            field_view = FieldFactory.string_field(
                field_name, _format_field_title(field_name)
            )
        elif field_type_str == "number":
            field_view = FieldFactory.number_field(
                field_name, _format_field_title(field_name)
            )
        elif field_type_str == "boolean":
            field_view = FieldFactory.boolean_field(
                field_name, _format_field_title(field_name)
            )
        elif field_type_str == "choice":
            field_view = FieldFactory.choice_field(
                field_name, _format_field_title(field_name)
            )
        elif field_type_str == "multichoice":
            field_view = FieldFactory.multichoice_field(
                field_name, _format_field_title(field_name)
            )
        else:
            field_view = FieldFactory.string_field(
                field_name, _format_field_title(field_name)
            )

        # Add validation if present
        if validation:
            field_view.validators = validation

        # Add help text if present
        help_text = _get_help_text(field_info)
        if help_text:
            field_view.help_text = help_text

        field_views.append(field_view)

    return field_views


def _get_field_type(python_type: Any) -> FieldType:
    """Convert Python type to FieldType."""
    origin = get_origin(python_type)

    # Handle UnionType for Python 3.10+
    if sys.version_info >= (3, 10):
        from types import UnionType

        if isinstance(python_type, UnionType):
            args = get_args(python_type)
            if type(None) in args:
                for arg in args:
                    if arg is not type(None):
                        return _get_field_type(arg)

    if origin is not None:
        # Handle Optional[T], Union[T, None], etc.
        args = get_args(python_type)
        if type(None) in args:
            # Find the non-None type
            for arg in args:
                if arg is not type(None):
                    return _get_field_type(arg)

        # Handle Literal types
        if origin is Literal:
            return "choice"

    # Type mapping for simple types
    type_mapping = {
        str: "string",
        int: "number",
        float: "number",
        bool: "boolean",
        list: "multichoice",  # Multi-select
    }

    # Check for list types with __origin__ attribute
    if (
        hasattr(python_type, "__origin__")
        and getattr(python_type, "__origin__") is list
    ):
        return "multichoice"

    # Return mapped type or default to string
    return cast(FieldType, type_mapping.get(python_type, "string"))


def _create_validation(field_info: Any) -> FieldValidation | None:
    """Create FieldValidation from SQLModel field info."""
    validation = FieldValidation()

    # Check for length constraints
    if hasattr(field_info, "max_length") and field_info.max_length:
        validation.max_length = field_info.max_length

    if hasattr(field_info, "min_length") and field_info.min_length:
        validation.min_length = field_info.min_length

    # Check for value constraints
    if hasattr(field_info, "gt") and field_info.gt is not None:
        validation.min_value = field_info.gt

    if hasattr(field_info, "gte") and field_info.gte is not None:
        validation.min_value = field_info.gte

    if hasattr(field_info, "lt") and field_info.lt is not None:
        validation.max_value = field_info.lt

    if hasattr(field_info, "lte") and field_info.lte is not None:
        validation.max_value = field_info.lte

    # Check for pattern validation (email, etc.)
    # Note: SQLModel Field doesn't support pattern directly
    # This would need to be handled through custom validation

    # Only return validation if we have some rules
    if any(
        [
            validation.min_length is not None,
            validation.max_length is not None,
            validation.min_value is not None,
            validation.max_value is not None,
            validation.pattern is not None,
        ]
    ):
        return validation

    return None


def _format_field_title(field_name: str) -> str:
    """Convert field name to human-readable title."""
    # Replace underscores with spaces and capitalize
    title = field_name.replace("_", " ").title()

    # Handle common abbreviations
    title = title.replace("Id", "ID")
    title = title.replace("Url", "URL")
    title = title.replace("Api", "API")

    return title


def _get_help_text(field_info: Any) -> str | None:
    """Extract help text from field info."""
    if hasattr(field_info, "description") and field_info.description:
        return cast(str, field_info.description)
    return None
