"""
Tests for error response JSON serialization.

This module tests that error responses can be properly serialized to JSON
without TypeError exceptions.
"""

import json

from fp_admin.admin.fields.errors import FieldError
from fp_admin.api.error_handlers import ErrorResponseBuilder
from fp_admin.exceptions import ValidationError


class TestErrorSerialization:
    """Test error response serialization."""

    def test_field_error_to_dict(self):
        """Test that FieldError can be converted to dictionary."""
        field_error = FieldError(
            code="FIELD_NOT_ALLOWED", message="Field 'test' is not allowed"
        )

        error_dict = field_error.to_dict()
        assert error_dict["code"] == "FIELD_NOT_ALLOWED"
        assert error_dict["message"] == "Field 'test' is not allowed"

        # Should be JSON serializable
        json_str = json.dumps(error_dict)
        assert "FIELD_NOT_ALLOWED" in json_str
        assert "Field 'test' is not allowed" in json_str

    def test_validation_error_with_field_errors(self):
        """Test that ValidationError with FieldError objects is serializable."""
        # Create a validation error with FieldError objects
        field_errors = {
            "username": [
                FieldError(
                    code="FIELD_NOT_ALLOWED", message="Field 'username' is not allowed"
                )
            ],
            "email": [
                FieldError(
                    code="FIELD_NOT_ALLOWED", message="Field 'email' is not allowed"
                )
            ],
        }

        validation_error = ValidationError(
            message="Validation failed", details={"field_errors": field_errors}
        )

        # Create error response
        error_response = ErrorResponseBuilder.field_validation_error(validation_error)

        # Should be JSON serializable
        json_str = json.dumps(error_response)
        assert "FIELD_NOT_ALLOWED" in json_str
        assert "Field 'username' is not allowed" in json_str
        assert "Field 'email' is not allowed" in json_str

    def test_validation_error_with_dict_errors(self):
        """Test that ValidationError with dictionary errors is serializable."""
        # Create a validation error with dictionary errors
        field_errors = {
            "username": [
                {
                    "code": "FIELD_NOT_ALLOWED",
                    "message": "Field 'username' is not allowed",
                }
            ],
            "email": [
                {"code": "FIELD_NOT_ALLOWED", "message": "Field 'email' is not allowed"}
            ],
        }

        validation_error = ValidationError(
            message="Validation failed", details={"field_errors": field_errors}
        )

        # Create error response
        error_response = ErrorResponseBuilder.field_validation_error(validation_error)

        # Should be JSON serializable
        json_str = json.dumps(error_response)
        assert "FIELD_NOT_ALLOWED" in json_str
        assert "Field 'username' is not allowed" in json_str
        assert "Field 'email' is not allowed" in json_str

    def test_mixed_error_types(self):
        """Test that mixed FieldError objects and dictionaries work together."""
        # Create a validation error with mixed types
        field_errors = {
            "username": [
                FieldError(
                    code="FIELD_NOT_ALLOWED", message="Field 'username' is not allowed"
                )
            ],
            "email": [
                {"code": "FIELD_NOT_ALLOWED", "message": "Field 'email' is not allowed"}
            ],
        }

        validation_error = ValidationError(
            message="Validation failed", details={"field_errors": field_errors}
        )

        # Create error response
        error_response = ErrorResponseBuilder.field_validation_error(validation_error)

        # Should be JSON serializable
        json_str = json.dumps(error_response)
        assert "FIELD_NOT_ALLOWED" in json_str
        assert "Field 'username' is not allowed" in json_str
        assert "Field 'email' is not allowed" in json_str

    def test_error_response_structure(self):
        """Test that error response has the correct structure."""
        field_errors = {
            "test_field": [
                FieldError(
                    code="FIELD_NOT_ALLOWED",
                    message="Field 'test_field' is not allowed",
                )
            ]
        }

        validation_error = ValidationError(
            message="Validation failed", details={"field_errors": field_errors}
        )

        error_response = ErrorResponseBuilder.field_validation_error(validation_error)

        # Check structure
        assert "type" in error_response
        assert "title" in error_response
        assert "status" in error_response
        assert "detail" in error_response
        assert "errors" in error_response

        # Check values
        assert error_response["type"] == "https://fp-admin.com/errors/field-validation"
        assert error_response["title"] == "Field Validation Error"
        assert error_response["status"] == 400
        assert error_response["detail"] == "One or more fields failed validation"

        # Check errors
        assert "test_field" in error_response["errors"]
        assert len(error_response["errors"]["test_field"]) == 1
        assert error_response["errors"]["test_field"][0]["code"] == "FIELD_NOT_ALLOWED"
        assert (
            error_response["errors"]["test_field"][0]["message"]
            == "Field 'test_field' is not allowed"
        )
