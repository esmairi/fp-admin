# Field validation functions extracted from FieldView
import re
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Union

from pydantic import BaseModel

from .errors import FieldError, get_error_message

if TYPE_CHECKING:
    from .base import FieldView


class FieldValidation(BaseModel):
    """Basic field validation rules."""

    required: bool = False
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    pattern: Optional[str] = None  # Regex pattern for validation


class FieldValidator:
    """Field validation factory class."""

    @classmethod
    def validate_value(cls, field_view: "FieldView", value: Any) -> List[FieldError]:
        """
        Main validation factory method.

        Args:
            field_view: The field view to validate against
            value: The value to validate

        Returns:
            List of FieldError objects (empty if valid)
        """
        errors: List[FieldError] = []
        # Skip further validation if value is empty and not required

        if not (field_view.validators and field_view.validators.required) and not value:
            return errors

        # Type-specific validation using mapping
        validation_map = {
            "string": cls.validate_string,
            "number": cls.validate_number,
            "float": cls.validate_float,
            "boolean": cls.validate_boolean,
            "date": cls.validate_date,
            "time": cls.validate_time,
            "datetime": cls.validate_datetime,
        }

        validator: Optional[Callable[["FieldView", Any], List[FieldError]]] = (
            validation_map.get(field_view.field_type)
        )
        if validator:
            errors.extend(validator(field_view, value))

        # Custom validation rules
        if field_view.validators:
            errors.extend(cls.validate_custom_rules(field_view, value))

        # Custom validator function
        if field_view.custom_validator:
            custom_error = field_view.custom_validator(value)
            if custom_error:
                errors.append(custom_error)

        return errors

    @classmethod
    def validate_custom_rules(
        cls, field_view: "FieldView", value: Any
    ) -> List[FieldError]:
        """Validate custom validation rules."""
        errors: List[FieldError] = []
        validators = field_view.validators

        if not validators:
            return errors
        # Check required field
        if validators.required and (value is None or value == ""):
            field_name = field_view.title or field_view.name
            errors.append(
                FieldError(
                    code="REQUIRED",
                    message=get_error_message("REQUIRED", field_name=field_name),
                )
            )

        if validators.min_length and len(str(value)) < validators.min_length:
            field_name = field_view.title or field_view.name
            errors.append(
                FieldError(
                    code="MIN_LENGTH",
                    message=get_error_message(
                        "MIN_LENGTH",
                        field_name=field_name,
                        min_length=validators.min_length,
                    ),
                )
            )

        if validators.max_length and len(str(value)) > validators.max_length:
            field_name = field_view.title or field_view.name
            errors.append(
                FieldError(
                    code="MAX_LENGTH",
                    message=get_error_message(
                        "MAX_LENGTH",
                        field_name=field_name,
                        max_length=validators.max_length,
                    ),
                )
            )

        # Only validate min_value for numeric fields
        if (
            validators.min_value is not None
            and field_view.field_type in ["number", "float"]
            and isinstance(value, (int, float))
        ):
            if value < validators.min_value:
                field_name = field_view.title or field_view.name
                errors.append(
                    FieldError(
                        code="MIN_VALUE",
                        message=get_error_message(
                            "MIN_VALUE",
                            field_name=field_name,
                            min_value=validators.min_value,
                        ),
                    )
                )

        # Only validate max_value for numeric fields
        if (
            validators.max_value is not None
            and field_view.field_type in ["number", "float"]
            and isinstance(value, (int, float))
        ):
            if value > validators.max_value:
                field_name = field_view.title or field_view.name
                errors.append(
                    FieldError(
                        code="MAX_VALUE",
                        message=get_error_message(
                            "MAX_VALUE",
                            field_name=field_name,
                            max_value=validators.max_value,
                        ),
                    )
                )

        if validators.pattern and not re.match(validators.pattern, str(value)):
            field_name = field_view.title or field_view.name
            errors.append(
                FieldError(
                    code="PATTERN",
                    message=get_error_message("PATTERN", field_name=field_name),
                )
            )

        return errors

    @classmethod
    def validate_string(cls, field_view: "FieldView", value: Any) -> List[FieldError]:
        """Validate string field value."""
        if not isinstance(value, str):
            field_name = field_view.title or field_view.name
            return [
                FieldError(
                    code="TYPE_STRING",
                    message=get_error_message("TYPE_STRING", field_name=field_name),
                )
            ]
        return []

    @classmethod
    def validate_number(cls, field_view: "FieldView", value: Any) -> List[FieldError]:
        """Validate number field value."""
        try:
            float(value)
        except (ValueError, TypeError):
            field_name = field_view.title or field_view.name
            return [
                FieldError(
                    code="TYPE_NUMBER",
                    message=get_error_message("TYPE_NUMBER", field_name=field_name),
                )
            ]
        return []

    @classmethod
    def validate_float(cls, field_view: "FieldView", value: Any) -> List[FieldError]:
        """Validate float field value."""
        try:
            float(value)
        except (ValueError, TypeError):
            field_name = field_view.title or field_view.name
            return [
                FieldError(
                    code="TYPE_NUMBER",
                    message=get_error_message("TYPE_NUMBER", field_name=field_name),
                )
            ]
        return []

    @classmethod
    def validate_boolean(cls, field_view: "FieldView", value: Any) -> List[FieldError]:
        """Validate boolean field value."""
        # Accept boolean, string "true"/"false", or 0/1
        if isinstance(value, bool):
            return []
        if isinstance(value, str) and value.lower() in ["true", "false"]:
            return []
        if isinstance(value, (int, float)) and value in [0, 1]:
            return []
        field_name = field_view.title or field_view.name
        return [
            FieldError(
                code="TYPE_BOOLEAN",
                message=get_error_message("TYPE_BOOLEAN", field_name=field_name),
            )
        ]

    @classmethod
    def validate_date(cls, field_view: "FieldView", value: Any) -> List[FieldError]:
        """Validate date field value."""
        if not isinstance(value, str):
            field_name = field_view.title or field_view.name
            return [
                FieldError(
                    code="TYPE_DATE",
                    message=get_error_message("TYPE_DATE", field_name=field_name),
                )
            ]
        return []

    @classmethod
    def validate_time(cls, field_view: "FieldView", value: Any) -> List[FieldError]:
        """Validate time field value."""
        if not isinstance(value, str):
            field_name = field_view.title or field_view.name
            return [
                FieldError(
                    code="TYPE_TIME",
                    message=get_error_message("TYPE_TIME", field_name=field_name),
                )
            ]
        return []

    @classmethod
    def validate_datetime(cls, field_view: "FieldView", value: Any) -> List[FieldError]:
        """Validate datetime field value."""
        if not isinstance(value, str):
            field_name = field_view.title or field_view.name
            return [
                FieldError(
                    code="TYPE_DATETIME",
                    message=get_error_message("TYPE_DATETIME", field_name=field_name),
                )
            ]
        return []
