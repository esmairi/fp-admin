"""
Base field classes for fp-admin.

This module provides the base field class and factory methods for creating form fields.
"""

from typing import Any, Callable, List, Optional, Type, TypedDict, Union

from pydantic import BaseModel
from sqlmodel import SQLModel

from .errors import FieldError
from .field_validator import FieldValidation, FieldValidator
from .types import FieldType
from .widgets import (
    DEFAULT_WIDGETS,
    WidgetConfig,
    WidgetType,
)


def get_default_widget(field_type: FieldType) -> WidgetType:
    """Get the default widget for a field type with proper typing."""
    return DEFAULT_WIDGETS.get(field_type, "text")


class FieldViewKwargs(TypedDict, total=False):
    """Keyword arguments for FieldView initialization."""

    help_text: Optional[str]
    widget: Optional[WidgetType]
    widget_config: Optional[WidgetConfig]
    required: bool
    readonly: bool
    disabled: bool
    placeholder: Optional[str]
    default_value: Optional[Any]
    options: Optional[dict[str, Any]]
    error: Optional[FieldError]
    validators: Optional[FieldValidation]
    custom_validator: Optional[Callable[[Any], Optional[FieldError]]]
    is_primary_key: bool
    model_class: Optional[Type[SQLModel]]
    # Validation parameters
    min_length: Optional[int]
    max_length: Optional[int]
    min_value: Optional[Union[int, float]]
    max_value: Optional[Union[int, float]]
    pattern: Optional[str]


class FieldView(BaseModel):
    """Form field specification for admin interface."""

    name: str
    title: Optional[str] = None
    model_class: Optional[Type[SQLModel]] = None
    help_text: Optional[str] = None
    field_type: FieldType
    widget: Optional[WidgetType] = None
    widget_config: Optional[WidgetConfig] = None
    required: bool = False
    readonly: bool = False
    disabled: bool = False
    placeholder: Optional[str] = None
    default_value: Optional[Any] = None
    options: Optional[dict[str, Any]] = None
    error: Optional[FieldError] = None
    validators: Optional[FieldValidation] = FieldValidation()
    custom_validator: Optional[Callable[[Any], Optional[FieldError]]] = None
    is_primary_key: bool = False

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize FieldView with proper typing.

        Args:
            **kwargs: Any valid field attributes for FieldView
        """
        super().__init__(**kwargs)
        # Set default widget if not provided and not explicitly set to None
        if self.widget is None and "widget" not in kwargs:
            self.widget = get_default_widget(self.field_type)

    def validate_value(self, value: Any) -> List[FieldError]:
        """
        Validate a field value and return list of FieldError objects.

        Args:
            value: The value to validate

        Returns:
            List of FieldError objects (empty if valid)
        """
        return FieldValidator.validate_value(self, value)
