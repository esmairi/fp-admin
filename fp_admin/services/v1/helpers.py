from typing import Any, Dict, List, Literal

from pydantic import BaseModel

from fp_admin.exceptions import ValidationError
from fp_admin.models.views.exceptions import (
    FieldErrorDetail,
    FpValidationErrors,
)
from fp_admin.registry import view_registry


class LookupFormResult(BaseModel):
    name: str
    extra_fields: int


def lookup_form_id(
    field_names: List[str], model_name: str, mode: Literal["create", "update"]
) -> str:
    """Return all 'form' views for `model_name` that contain all `field_names`,
    keeping only those with the fewest extra fields required."""

    def _fail() -> None:
        raise ValueError(f"Failed to load form for: {model_name}")

    views = view_registry.get(model_name) or []
    forms = [v for v in views if getattr(v, "view_type", None) == "form"]
    if not forms:
        _fail()

    required = set(field_names)

    candidates: List[LookupFormResult] = []
    for form in forms:
        if mode == "create":
            target_fields = set(form.creation_fields)
        elif mode == "update":
            target_fields = set(form.allowed_update_fields)
        else:
            raise ValueError(f"Unknown mode: {mode}")
        if required.issubset(target_fields):
            extra = len(target_fields - required)
            candidates.append(LookupFormResult(name=form.name, extra_fields=extra))

    if not candidates:
        _fail()
    min_extra = min(c.extra_fields for c in candidates)
    return [c for c in candidates if c.extra_fields == min_extra][0].name


def validate_allowed_fields(
    form_id: str, data: Dict[str, Any], mode: Literal["create", "update"]
) -> None:
    """Validate that only allowed fields are provided."""
    form = view_registry.get_form_view(form_id)
    if mode == "create":
        target_fields = set(form.creation_fields)
    elif mode == "update":
        target_fields = set(form.allowed_update_fields)
    else:
        raise ValueError(f"Unknown mode: {mode}")
    non_allowed_fields = set(data.keys()) - target_fields
    if non_allowed_fields:
        field_errors = [
            FieldErrorDetail(
                code="FIELD_NOT_ALLOWED",
                message=f"Field '{field_name}' is not allowed",
                field_name=field_name,
            )
            for field_name in non_allowed_fields
        ]
        raise FpValidationErrors(field_errors)


def raise_serialized_validation_error(
    message: str, field_errors: Dict[str, Any]
) -> None:
    """Raise ValidationError with serialized field errors."""
    error_response = {"errors": serialize_field_errors(field_errors)}
    raise ValidationError(message=message, details=error_response)


def serialize_field_errors(
    field_errors: Dict[str, Any],
) -> Dict[str, List[Dict[str, str]]]:
    """
    Convert FieldError objects or dicts to serializable dicts.

    This function handles the common pattern of serializing field errors
    that can be either FieldError objects, dictionaries, or other error types.

    Args:
        field_errors: Dictionary mapping field names to error lists

    Returns:
        Dictionary with serialized error information
    """
    serialized_errors: Dict[str, List[Dict[str, str]]] = {}
    for field_name, errors in field_errors.items():
        serialized_errors[field_name] = []
        for error in errors:
            if hasattr(error, "to_dict"):
                # FieldError object
                serialized_errors[field_name].append(error.to_dict())
            elif isinstance(error, dict):
                # Already a dictionary
                serialized_errors[field_name].append(error)
            else:
                # Fallback: try to convert to dict
                serialized_errors[field_name].append(
                    {
                        "code": getattr(error, "code", "UNKNOWN").upper(),
                        "message": getattr(error, "message", str(error)),
                    }
                )
    return serialized_errors
