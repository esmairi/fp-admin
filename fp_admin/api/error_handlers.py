"""
Error handling utilities for fp-admin API.

This module provides standardized error response formatting
"""

from typing import Any, Dict, List

from fastapi import HTTPException

from fp_admin.models.views.exceptions import FieldErrorDetail


def handle_validation_error(errors: List[FieldErrorDetail]) -> HTTPException:
    """
    Handle ValidationError and return standardized HTTPException.

    Args:
        errors: The ValidationError exception

    Returns:
        HTTPException
    """
    error_response = {
        "type": "https://fp-admin.com/errors/field-validation",
        "title": "Field Validation Error",
        "status": 400,
        "errors": [err.model_dump() for err in errors],
    }
    return HTTPException(status_code=400, detail=error_response)


class ErrorResponseBuilder:
    """Builder for standardized error responses following RFC 7807."""

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
            "errors": f"{resource.capitalize()} '{identifier}' not found",
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


def handle_record_error(message: str) -> HTTPException:
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
