"""
Field errors for fp-admin.

This module provides error handling for form fields.
"""

from typing import Any

from pydantic import BaseModel


class FieldError(BaseModel):
    """Field validation error."""

    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        """Convert FieldError to dictionary for JSON serialization."""
        return {"code": self.code.upper(), "message": self.message}

    def __hash__(self) -> int:
        """Make FieldError hashable."""
        return hash((self.code, self.message))

    def __eq__(self, other: object) -> bool:
        """Compare FieldError instances."""
        if not isinstance(other, FieldError):
            return False
        return self.code == other.code and self.message == other.message


# Error message constants
ERROR_MESSAGES = {
    "REQUIRED": "{field_name} is required",
    "TYPE_STRING": "{field_name} must be a string",
    "TYPE_NUMBER": "{field_name} must be a number",
    "TYPE_BOOLEAN": "{field_name} must be a boolean",
    "TYPE_DATE": "{field_name} must be a date string",
    "TYPE_TIME": "{field_name} must be a time string",
    "TYPE_DATETIME": "{field_name} must be a datetime string",
    "MIN_LENGTH": "{field_name} must be at least {min_length} characters",
    "MAX_LENGTH": "{field_name} must be no more than {max_length} characters",
    "MIN_VALUE": "{field_name} must be at least {min_value}",
    "MAX_VALUE": "{field_name} must be no more than {max_value}",
    "PATTERN": "{field_name} format is invalid",
    "NOT_FOUND": "Form '{form_id}' not found",
}


def get_error_message(code: str, **kwargs: Any) -> str:
    """Get error message for a given code with optional formatting."""
    message_template = ERROR_MESSAGES.get(code, "{field_name} validation failed")
    # Provide default field_name if not provided
    if "field_name" not in kwargs:
        kwargs["field_name"] = "Field"
    return message_template.format(**kwargs)
