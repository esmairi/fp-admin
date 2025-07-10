"""
Unit tests for field errors.

This module tests the FieldError class and error message handling functionality.
"""

from fp_admin.admin.fields.errors import FieldError, get_error_message


class TestFieldError:
    """Test cases for FieldError class."""

    def test_field_error_to_dict(self):
        """Test FieldError to_dict method."""
        error = FieldError(code="REQUIRED", message="Field is required")
        error_dict = error.to_dict()

        assert error_dict["code"] == "REQUIRED"

    def test_field_error_serialization(self):
        """Test FieldError serialization to dict."""
        error = FieldError(code="MIN_LENGTH", message="Too short")
        error_dict = error.model_dump()

        assert error_dict["code"] == "MIN_LENGTH"
        assert error_dict["message"] == "Too short"


class TestGetErrorMessage:
    """Test cases for get_error_message function."""

    def test_get_error_message_required(self):
        """Test getting error message for REQUIRED code."""
        message = get_error_message("REQUIRED", field_name="Username")
        assert message == "Username is required"

    def test_get_error_message_type_string(self):
        """Test getting error message for TYPE_STRING code."""
        message = get_error_message("TYPE_STRING", field_name="Email")
        assert message == "Email must be a string"

    def test_get_error_message_type_number(self):
        """Test getting error message for TYPE_NUMBER code."""
        message = get_error_message("TYPE_NUMBER", field_name="Age")
        assert message == "Age must be a number"

    def test_get_error_message_type_boolean(self):
        """Test getting error message for TYPE_BOOLEAN code."""
        message = get_error_message("TYPE_BOOLEAN", field_name="Active")
        assert message == "Active must be a boolean"

    def test_get_error_message_type_date(self):
        """Test getting error message for TYPE_DATE code."""
        message = get_error_message("TYPE_DATE", field_name="Birth Date")
        assert message == "Birth Date must be a date string"

    def test_get_error_message_type_time(self):
        """Test getting error message for TYPE_TIME code."""
        message = get_error_message("TYPE_TIME", field_name="Start Time")
        assert message == "Start Time must be a time string"

    def test_get_error_message_type_datetime(self):
        """Test getting error message for TYPE_DATETIME code."""
        message = get_error_message("TYPE_DATETIME", field_name="Created At")
        assert message == "Created At must be a datetime string"

    def test_get_error_message_min_length(self):
        """Test getting error message for MIN_LENGTH code."""
        message = get_error_message("MIN_LENGTH", field_name="Password", min_length=8)
        assert message == "Password must be at least 8 characters"

    def test_get_error_message_max_length(self):
        """Test getting error message for MAX_LENGTH code."""
        message = get_error_message(
            "MAX_LENGTH", field_name="Description", max_length=100
        )
        assert message == "Description must be no more than 100 characters"

    def test_get_error_message_min_value(self):
        """Test getting error message for MIN_VALUE code."""
        message = get_error_message("MIN_VALUE", field_name="Age", min_value=18)
        assert message == "Age must be at least 18"

    def test_get_error_message_max_value(self):
        """Test getting error message for MAX_VALUE code."""
        message = get_error_message("MAX_VALUE", field_name="Score", max_value=100)
        assert message == "Score must be no more than 100"

    def test_get_error_message_pattern(self):
        """Test getting error message for PATTERN code."""
        message = get_error_message("PATTERN", field_name="Email")
        assert message == "Email format is invalid"

    def test_get_error_message_not_found(self):
        """Test getting error message for NOT_FOUND code."""
        message = get_error_message("NOT_FOUND", form_id="user_form")
        assert message == "Form 'user_form' not found"

    def test_get_error_message_unknown_code(self):
        """Test getting error message for unknown code."""
        message = get_error_message("UNKNOWN_CODE", field_name="Test Field")
        assert message == "Test Field validation failed"

    def test_get_error_message_with_kwargs(self):
        """Test getting error message with multiple kwargs."""
        message = get_error_message(
            "MIN_LENGTH", field_name="Password", min_length=8, custom_param="test"
        )
        assert message == "Password must be at least 8 characters"

    def test_get_error_message_empty_kwargs(self):
        """Test getting error message with empty kwargs."""
        message = get_error_message("REQUIRED")
        assert message == "Field is required"
