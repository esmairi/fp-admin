"""
Field specifications for fp-admin.

This package provides field types, validation rules, and field specifications
used throughout the admin interface for form generation.
"""

from .base import FieldView
from .errors import FieldError
from .field_factory import FieldFactory
from .field_validator import FieldValidation
from .types import FieldType
from .widgets import (
    DEFAULT_WIDGETS,
    WidgetConfig,
    WidgetType,
    validate_widget_combination,
)

__all__ = [
    # Field types
    "FieldType",
    # Validation
    "FieldValidation",
    # Field components
    "FieldError",
    # Field classes
    "FieldView",
    "FieldFactory",
    # Widget types
    "WidgetType",
    "WidgetConfig",
    "DEFAULT_WIDGETS",
    "validate_widget_combination",
]
