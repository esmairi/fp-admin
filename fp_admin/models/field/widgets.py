"""
Widget types for fp-admin.

This module defines the widget types that can be used to render different field types
in the admin interface.
"""

from typing import Literal, Optional, Union

from pydantic import BaseModel

# Widget types for different field types
StringWidget = Literal["text", "textarea", "password"]
NumberWidget = Literal["input", "Slider"]
DateWidget = Literal["calendar"]
BooleanWidget = Literal["Checkbox", "switch", "select"]
ChoiceWidget = Literal["dropdown", "radio", "select"]
MultiChoiceWidget = Literal["multiSelect", "chips", "listBox"]
RelationshipWidget = Literal["dropdown", "autoComplete"]
FileWidget = Literal["upload", "image"]
JsonWidget = Literal["editor"]
ColorWidget = Literal["colorPicker"]

# Union of all widget types
WidgetType = Union[
    StringWidget,
    NumberWidget,
    DateWidget,
    BooleanWidget,
    ChoiceWidget,
    MultiChoiceWidget,
    RelationshipWidget,
    FileWidget,
    JsonWidget,
    ColorWidget,
]

# All widget types as strings for testing
WIDGET_TYPES = {
    "text",
    "textarea",
    "password",  # String widgets
    "input",
    "Slider",  # Number widgets
    "calendar",  # Date widgets
    "Checkbox",
    "switch",
    "dropdown",
    "radio",
    "select",  # Choice widgets
    "multiSelect",
    "chips",
    "listBox",  # Multi-choice widgets
    "autoComplete",  # Relationship widgets
    "upload",
    "image",  # File widgets
    "editor",  # JSON widgets
    "colorPicker",  # Color widgets
}


# Widget configuration options
class WidgetConfig(BaseModel):
    """Configuration options for widgets."""

    timeOnly: bool = False  # For time fields
    showTime: bool = False  # For datetime fields
    mode: str = "decimal"  # For float fields
    preview: bool = False  # For image fields
    editor_type: str = "monaco"  # For JSON fields
    accept: Optional[str] = None  # For file/image fields
    min: Optional[float] = None  # For number/float fields
    max: Optional[float] = None  # For number/float fields
    step: Optional[float] = None  # For number/float fields


# Valid widget combinations for field types
VALID_WIDGET_COMBINATIONS = {
    "string": ["text", "textarea", "password"],
    "number": ["input", "Slider"],
    "float": ["input", "Slider"],
    "time": ["calendar"],
    "datetime": ["calendar"],
    "boolean": ["Checkbox", "switch", "select"],
    "choice": ["dropdown", "radio", "select"],
    "multichoice": ["multiSelect", "chips", "listBox"],
    "foreignkey": ["dropdown", "autoComplete"],
    "many_to_many": ["autoComplete", "dropdown"],
    "OneToOneField": ["autoComplete", "dropdown"],
    "date": ["calendar"],
    "file": ["upload"],
    "image": ["image"],
    "json": ["editor"],
    "color": ["colorPicker"],
    "primarykey": ["text"],
}

# Default widget mappings for field types
DEFAULT_WIDGETS: dict[str, WidgetType] = {
    "string": "text",
    "number": "input",
    "float": "input",
    "time": "calendar",
    "datetime": "calendar",
    "boolean": "Checkbox",
    "choice": "dropdown",
    "multichoice": "multiSelect",
    "foreignkey": "dropdown",
    "many_to_many": "autoComplete",
    "OneToOneField": "dropdown",
    "date": "calendar",
    "file": "upload",
    "image": "image",
    "json": "editor",
    "color": "colorPicker",
    "primary_key": "text",
    "password": "text",
}
