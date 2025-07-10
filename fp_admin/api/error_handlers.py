"""
Error handling utilities for fp-admin API.

This module provides standardized error response formatting
following RFC 7807 Problem Details standard.
"""

from typing import Any, Dict

from fastapi import HTTPException

from fp_admin.exceptions import ValidationError


class ErrorResponseBuilder:
    """Builder for standardized error responses following RFC 7807."""

    @staticmethod
    def field_validation_error(validation_error: ValidationError) -> Dict[str, Any]:
        """
        Create a field validation error response.

        Args:
            validation_error: The ValidationError exception

        Returns:
            RFC 7807 compliant error response
        """
        # Handle both "errors" and "field_errors" keys for compatibility
        field_errors = validation_error.details.get("errors", {})
        if not field_errors:
            field_errors = validation_error.details.get("field_errors", {})

        # Convert FieldError objects to dictionaries if needed
        serialized_errors: dict[str, list[dict[str, str]]] = {}
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

        return {
            "type": "https://fp-admin.com/errors/field-validation",
            "title": "Field Validation Error",
            "status": 400,
            "detail": "One or more fields failed validation",
            "errors": serialized_errors,
        }

    @staticmethod
    def model_error(message: str) -> Dict[str, Any]:
        """
        Create a model operation error response.

        Args:
            message: The error message

        Returns:
            RFC 7807 compliant error response
        """
        return {
            "type": "https://fp-admin.com/errors/model-operation",
            "title": "Model Operation Error",
            "status": 400,
            "detail": message,
        }

    @staticmethod
    def not_found_error(resource: str, identifier: str) -> Dict[str, Any]:
        """
        Create a not found error response.

        Args:
            resource: The resource type (e.g., "model", "record")
            identifier: The identifier that wasn't found

        Returns:
            RFC 7807 compliant error response
        """
        return {
            "type": "https://fp-admin.com/errors/not-found",
            "title": "Resource Not Found",
            "status": 404,
            "detail": f"{resource.capitalize()} '{identifier}' not found",
        }

    @staticmethod
    def server_error(message: str = "Internal server error") -> Dict[str, Any]:
        """
        Create a server error response.

        Args:
            message: The error message

        Returns:
            RFC 7807 compliant error response
        """
        return {
            "type": "https://fp-admin.com/errors/server-error",
            "title": "Internal Server Error",
            "status": 500,
            "detail": message,
        }


def handle_validation_error(validation_error: ValidationError) -> HTTPException:
    """
    Handle ValidationError and return standardized HTTPException.

    Args:
        validation_error: The ValidationError exception

    Returns:
        HTTPException with RFC 7807 compliant error response
    """
    error_response = ErrorResponseBuilder.field_validation_error(validation_error)
    return HTTPException(status_code=400, detail=error_response)


def handle_model_error(message: str) -> HTTPException:
    """
    Handle ModelError and return standardized HTTPException.

    Args:
        message: The error message

    Returns:
        HTTPException with RFC 7807 compliant error response
    """
    error_response = ErrorResponseBuilder.model_error(message)
    return HTTPException(status_code=400, detail=error_response)


def handle_not_found_error(resource: str, identifier: str) -> HTTPException:
    """
    Handle not found errors and return standardized HTTPException.

    Args:
        resource: The resource type (e.g., "model", "record")
        identifier: The identifier that wasn't found

    Returns:
        HTTPException with RFC 7807 compliant error response
    """
    error_response = ErrorResponseBuilder.not_found_error(resource, identifier)
    return HTTPException(status_code=404, detail=error_response)


def handle_server_error(message: str = "Internal server error") -> HTTPException:
    """
    Handle server errors and return standardized HTTPException.

    Args:
        message: The error message

    Returns:
        HTTPException with RFC 7807 compliant error response
    """
    error_response = ErrorResponseBuilder.server_error(message)
    return HTTPException(status_code=500, detail=error_response)
