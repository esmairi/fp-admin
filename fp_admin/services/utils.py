from typing import Any, Dict, List, Type

from sqlalchemy.inspection import inspect
from sqlmodel import SQLModel

from fp_admin.admin.models import model_registry
from fp_admin.exceptions import ModelError, ValidationError


def get_relationship_fields(model_class: Type[SQLModel]) -> List[str]:
    """Get all relationship field names from a model.

    Args:
        model_class: The model class

    Returns:
        List of relationship field names
    """

    mapper = inspect(model_class)
    if not mapper:
        raise ModelError("ERROR: INSPECT MODEL")
    return list(mapper.relationships.keys())


def get_model_class(model_name: str) -> Type[SQLModel]:
    """Get model class from registry and validate it exists.

    Args:
        model_name: Name of the model to get

    Returns:
        The model class

    Raises:
        ModelError: If model is not found in registry
    """
    model_class = model_registry.get_model_class(model_name)
    if not model_class:
        raise ModelError(f"Model [{model_name}] not found in registry")
    return model_class


def serialize_field_errors(
    field_errors: Dict[str, Any],
) -> Dict[str, List[Dict[str, str]]]:
    """Convert FieldError objects or dicts to serializable dicts."""
    serialized_errors: Dict[str, List[Dict[str, str]]] = {}
    for field_name, errors in field_errors.items():
        serialized_errors[field_name] = []
        for error in errors:
            if hasattr(error, "to_dict"):
                serialized_errors[field_name].append(error.to_dict())
            elif isinstance(error, dict):
                serialized_errors[field_name].append(error)
            else:
                serialized_errors[field_name].append(
                    {
                        "code": getattr(error, "code", "UNKNOWN").upper(),
                        "message": getattr(error, "message", str(error)),
                    }
                )
    return serialized_errors


def raise_serialized_validation_error(
    message: str, field_errors: Dict[str, Any]
) -> None:
    """Raise ValidationError with serialized field errors."""
    error_response = {"errors": serialize_field_errors(field_errors)}
    raise ValidationError(message=message, details=error_response)


def validate_allowed_fields(
    model_name: str, data: Dict[str, Any], mode: str = "creation"
) -> None:
    """Validate that only allowed fields are provided.

    Args:
        model_name: Name of the model
        data: Data to validate
        mode: Type of fields to check ("creation" or "update")
    """
    from fp_admin.admin.views import view_registry

    modes = {
        "creation": "creation_fields",
        "update": "allowed_update_fields",
    }
    model_views = view_registry.get(model_name)
    if model_views is None:
        return

    for view in model_views:
        field_attr = modes[mode]
        allowed_fields = getattr(view, field_attr, None)
        if allowed_fields:
            allowed_field_names = set(allowed_fields)
            non_allowed_fields = set(data.keys()) - allowed_field_names
            if non_allowed_fields:
                field_errors = {
                    field_name: [
                        {
                            "code": "FIELD_NOT_ALLOWED",
                            "message": (
                                f"Field '{field_name}' is not allowed " f"to be {mode}d"
                            ),
                        }
                    ]
                    for field_name in non_allowed_fields
                }
                raise ValidationError(
                    message=f"{mode.capitalize()} validation failed",
                    details={"field_errors": field_errors},
                )
