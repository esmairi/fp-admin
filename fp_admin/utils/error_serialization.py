"""
Error serialization utilities for fp-admin.

This module provides shared utilities for serializing field errors
to eliminate duplicate code across the codebase.
"""

from typing import Any, Dict, List


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
