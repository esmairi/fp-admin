"""
Unit tests for field errors.

Tests the FieldError class and error handling.
"""

import pytest
from pydantic import ValidationError

from fp_admin.admin.fields.errors import FieldError

pytestmark = pytest.mark.unit


class TestFieldError:
    """Test cases for FieldError."""

    def test_field_error_creation(self) -> None:
        """Test basic FieldError creation."""
        error = FieldError(code="required", message="This field is required")

        assert error.code == "required"
        assert error.message == "This field is required"

    def test_field_error_required_fields(self) -> None:
        """Test that code and message are required fields."""
        # Should work with both fields
        error = FieldError(code="invalid", message="Invalid value")
        assert error.code == "invalid"
        assert error.message == "Invalid value"

    def test_field_error_missing_code(self) -> None:
        """Test that code field is required."""
        with pytest.raises(ValidationError):
            FieldError(message="This field is required")

    def test_field_error_missing_message(self) -> None:
        """Test that message field is required."""
        with pytest.raises(ValidationError):
            FieldError(code="required")

    def test_field_error_empty_strings(self) -> None:
        """Test that empty strings are allowed."""
        error = FieldError(code="", message="")

        assert error.code == ""
        assert error.message == ""

    def test_field_error_unicode(self) -> None:
        """Test that unicode characters are handled correctly."""
        error = FieldError(
            code="unicode_error", message="Erreur avec des caractères spéciaux: éàçù"
        )

        assert error.code == "unicode_error"
        assert error.message == "Erreur avec des caractères spéciaux: éàçù"

    def test_field_error_long_message(self) -> None:
        """Test that long error messages are handled."""
        long_message = (
            "This is a very long error message that contains many characters"
            " and should be handled properly by the FieldError class without any issues"
        )
        error = FieldError(code="long_error", message=long_message)

        assert error.code == "long_error"
        assert error.message == long_message

    def test_field_error_serialization(self) -> None:
        """Test that FieldError can be serialized to dict."""
        error = FieldError(code="test", message="Test error message")

        data = error.model_dump()

        assert data["code"] == "test"
        assert data["message"] == "Test error message"

    def test_field_error_from_dict(self) -> None:
        """Test that FieldError can be created from dict."""
        data = {"code": "validation_error", "message": "Validation failed"}

        error = FieldError(**data)

        assert error.code == "validation_error"
        assert error.message == "Validation failed"

    def test_field_error_equality(self) -> None:
        """Test that FieldError instances can be compared."""
        error1 = FieldError(code="same", message="Same message")
        error2 = FieldError(code="same", message="Same message")
        error3 = FieldError(code="different", message="Different message")

        assert error1 == error2
        assert error1 != error3

    def test_field_error_repr(self) -> None:
        """Test that FieldError has a meaningful string representation."""
        error = FieldError(code="test_code", message="Test message")

        repr_str = repr(error)

        assert "FieldError" in repr_str
        assert "test_code" in repr_str
        assert "Test message" in repr_str

    def test_field_error_str(self) -> None:
        """Test that FieldError has a meaningful string representation."""
        error = FieldError(code="test_code", message="Test message")

        str_repr = str(error)

        assert "test_code" in str_repr
        assert "Test message" in str_repr
