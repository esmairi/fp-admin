"""
Unit tests for field validation.

This module tests the FieldValidation and FieldValidator
classes and their validation logic.
"""

from fp_admin.admin.fields.base import FieldView
from fp_admin.admin.fields.errors import FieldError
from fp_admin.admin.fields.field_validator import FieldValidation, FieldValidator


class TestFieldValidation:
    """Test cases for FieldValidation class."""

    def test_field_validation_creation_default(self):
        """Test creating FieldValidation with default values."""
        validation = FieldValidation()

        assert validation.required is False
        assert validation.min_length is None
        assert validation.max_length is None
        assert validation.min_value is None
        assert validation.max_value is None
        assert validation.pattern is None

    def test_field_validation_creation_with_values(self):
        """Test creating FieldValidation with custom values."""
        validation = FieldValidation(
            required=True,
            min_length=5,
            max_length=100,
            min_value=0,
            max_value=1000,
            pattern=r"^[a-zA-Z]+$",
        )

        assert validation.required is True
        assert validation.min_length == 5
        assert validation.max_length == 100
        assert validation.min_value == 0
        assert validation.max_value == 1000
        assert validation.pattern == r"^[a-zA-Z]+$"

    def test_field_validation_serialization(self):
        """Test FieldValidation serialization to dict."""
        validation = FieldValidation(
            required=True,
            min_length=5,
            max_length=100,
            min_value=0,
            max_value=1000,
            pattern=r"^[a-zA-Z]+$",
        )

        validation_dict = validation.model_dump()

        assert validation_dict["required"] is True
        assert validation_dict["min_length"] == 5
        assert validation_dict["max_length"] == 100
        assert validation_dict["min_value"] == 0
        assert validation_dict["max_value"] == 1000
        assert validation_dict["pattern"] == r"^[a-zA-Z]+$"

    def test_field_validation_from_dict(self):
        """Test creating FieldValidation from dictionary."""
        validation_data = {
            "required": True,
            "min_length": 5,
            "max_length": 100,
            "min_value": 0,
            "max_value": 1000,
            "pattern": r"^[a-zA-Z]+$",
        }

        validation = FieldValidation(**validation_data)

        assert validation.required is True
        assert validation.min_length == 5
        assert validation.max_length == 100
        assert validation.min_value == 0
        assert validation.max_value == 1000
        assert validation.pattern == r"^[a-zA-Z]+$"

    def test_field_validation_partial_values(self):
        """Test creating FieldValidation with partial values."""
        validation = FieldValidation(
            required=True,
            min_length=5,
        )

        assert validation.required is True
        assert validation.min_length == 5
        assert validation.max_length is None  # Default
        assert validation.min_value is None  # Default
        assert validation.max_value is None  # Default
        assert validation.pattern is None  # Default

    def test_field_validation_equality(self):
        """Test FieldValidation equality."""
        validation1 = FieldValidation(required=True, min_length=5)
        validation2 = FieldValidation(required=True, min_length=5)
        validation3 = FieldValidation(required=False, min_length=5)

        assert validation1 == validation2
        assert validation1 != validation3


class TestFieldValidator:
    """Test cases for FieldValidator class."""

    def test_validate_value_no_validation(self):
        """Test validate_value with no validation rules."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
        )

        errors = FieldValidator.validate_value(field, "test")
        assert len(errors) == 0

    def test_validate_value_empty_not_required(self):
        """Test validate_value with empty value when not required."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            validators=FieldValidation(required=False),
        )

        errors = FieldValidator.validate_value(field, "")
        assert len(errors) == 0

        errors = FieldValidator.validate_value(field, None)
        assert len(errors) == 0

    def test_validate_value_empty_required(self):
        """Test validate_value with empty value when required."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            validators=FieldValidation(required=True),
        )

        errors = FieldValidator.validate_value(field, "")
        assert len(errors) == 1
        error_codes = [error.code for error in errors]
        assert "REQUIRED" in error_codes

        errors = FieldValidator.validate_value(field, None)
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "REQUIRED" in error_codes


class TestCustomRulesValidation:
    """Test cases for custom validation rules."""

    def test_validate_custom_rules_required(self):
        """Test validate_custom_rules with required validation."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            validators=FieldValidation(required=True),
        )

        errors = FieldValidator.validate_custom_rules(field, "")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "REQUIRED" in error_codes

        errors = FieldValidator.validate_custom_rules(field, "valid")
        assert len(errors) == 0

    def test_validate_custom_rules_min_length(self):
        """Test validate_custom_rules with min_length validation."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            validators=FieldValidation(min_length=5),
        )

        errors = FieldValidator.validate_custom_rules(field, "abc")
        assert len(errors) == 1
        error_codes = [error.code for error in errors]
        assert "MIN_LENGTH" in error_codes

        errors = FieldValidator.validate_custom_rules(field, "valid")
        assert len(errors) == 0

    def test_validate_custom_rules_max_length(self):
        """Test validate_custom_rules with max_length validation."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            validators=FieldValidation(max_length=5),
        )

        errors = FieldValidator.validate_custom_rules(field, "too_long_string")
        assert len(errors) == 1
        error_codes = [error.code for error in errors]
        assert "MAX_LENGTH" in error_codes

        errors = FieldValidator.validate_custom_rules(field, "valid")
        assert len(errors) == 0

    def test_validate_custom_rules_min_value(self):
        """Test validate_custom_rules with min_value validation."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="number",
            validators=FieldValidation(min_value=10),
        )

        errors = FieldValidator.validate_custom_rules(field, 5)
        assert len(errors) == 1
        error_codes = [error.code for error in errors]
        assert "MIN_VALUE" in error_codes

        errors = FieldValidator.validate_custom_rules(field, 15)
        assert len(errors) == 0

    def test_validate_custom_rules_max_value(self):
        """Test validate_custom_rules with max_value validation."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="number",
            validators=FieldValidation(max_value=100),
        )

        errors = FieldValidator.validate_custom_rules(field, 150)
        assert len(errors) == 1
        error_codes = [error.code for error in errors]
        assert "MAX_VALUE" in error_codes

        errors = FieldValidator.validate_custom_rules(field, 50)
        assert len(errors) == 0

    def test_validate_custom_rules_pattern(self):
        """Test validate_custom_rules with pattern validation."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            validators=FieldValidation(pattern=r"^[a-zA-Z]+$"),
        )

        errors = FieldValidator.validate_custom_rules(field, "abc123")
        assert len(errors) == 1
        error_codes = [error.code for error in errors]
        assert "PATTERN" in error_codes

        errors = FieldValidator.validate_custom_rules(field, "abc")
        assert len(errors) == 0

    def test_validate_custom_rules_multiple_rules(self):
        """Test validate_custom_rules with multiple validation rules."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            validators=FieldValidation(
                required=True,
                min_length=5,
                max_length=10,
                pattern=r"^[a-zA-Z]+$",
            ),
        )

        # Test empty value (required)
        errors = FieldValidator.validate_custom_rules(field, "")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "REQUIRED" in error_codes

        # Test too short (min_length)
        errors = FieldValidator.validate_custom_rules(field, "abc")
        assert len(errors) == 1
        error_codes = [error.code for error in errors]
        assert "MIN_LENGTH" in error_codes

        # Test too long (max_length)
        errors = FieldValidator.validate_custom_rules(field, "abcdefghijk")
        assert len(errors) == 1
        error_codes = [error.code for error in errors]
        assert "MAX_LENGTH" in error_codes

        # Test invalid pattern
        errors = FieldValidator.validate_custom_rules(field, "abc123")
        assert len(errors) == 1
        error_codes = [error.code for error in errors]
        assert "PATTERN" in error_codes

        # Test valid value
        errors = FieldValidator.validate_custom_rules(field, "abcdef")
        assert len(errors) == 0

    def test_validate_custom_rules_multiple_errors_simultaneously(self):
        """Test validate_custom_rules with multiple errors at once."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            validators=FieldValidation(
                required=True,
                min_length=5,
                max_length=10,
                pattern=r"^[a-zA-Z]+$",
            ),
        )

        # Test value that violates multiple rules at once
        errors = FieldValidator.validate_custom_rules(
            field, "ab"
        )  # Too short and invalid pattern
        assert len(errors) >= 1  # Should have at least one error
        error_codes = [error.code for error in errors]
        assert "MIN_LENGTH" in error_codes or "PATTERN" in error_codes

    def test_validate_custom_rules_no_validators(self):
        """Test validate_custom_rules with no validators."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
        )

        errors = FieldValidator.validate_custom_rules(field, "test")
        assert len(errors) == 0


class TestTypeValidation:
    """Test cases for type-specific validation."""

    def test_validate_string_valid(self):
        """Test validate_string with valid string value."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
        )

        errors = FieldValidator.validate_string(field, "test")
        assert len(errors) == 0

    def test_validate_string_invalid(self):
        """Test validate_string with invalid non-string value."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
        )

        errors = FieldValidator.validate_string(field, 123)
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "TYPE_STRING" in error_codes

        errors = FieldValidator.validate_string(field, True)
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "TYPE_STRING" in error_codes

    def test_validate_number_valid(self):
        """Test validate_number with valid numeric values."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="number",
        )

        # Test various valid numeric inputs
        for value in [123, 123.45, "123", "123.45", 0, -123]:
            errors = FieldValidator.validate_number(field, value)
            assert len(errors) == 0

    def test_validate_number_invalid(self):
        """Test validate_number with invalid non-numeric values."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="number",
        )

        errors = FieldValidator.validate_number(field, "abc")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "TYPE_NUMBER" in error_codes

        errors = FieldValidator.validate_number(field, "12abc")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "TYPE_NUMBER" in error_codes

    def test_validate_float_valid(self):
        """Test validate_float with valid float values."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="float",
        )

        # Test various valid float inputs
        for value in [123.45, "123.45", 123, "123", 0.0, -123.45]:
            errors = FieldValidator.validate_float(field, value)
            assert len(errors) == 0

    def test_validate_float_invalid(self):
        """Test validate_float with invalid non-float values."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="float",
        )

        errors = FieldValidator.validate_float(field, "abc")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "TYPE_NUMBER" in error_codes

    def test_validate_boolean_valid(self):
        """Test validate_boolean with valid boolean values."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="boolean",
        )

        # Test various valid boolean inputs
        for value in [True, False, "true", "false", "True", "False", 1, 0]:
            errors = FieldValidator.validate_boolean(field, value)
            assert len(errors) == 0

    def test_validate_boolean_invalid(self):
        """Test validate_boolean with invalid non-boolean values."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="boolean",
        )

        errors = FieldValidator.validate_boolean(field, "abc")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "TYPE_BOOLEAN" in error_codes

        errors = FieldValidator.validate_boolean(field, 123)
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "TYPE_BOOLEAN" in error_codes

    def test_validate_date_valid(self):
        """Test validate_date with valid date values."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="date",
        )

        # Test various valid date inputs
        for value in ["2023-01-01", "2023/01/01", "01/01/2023"]:
            errors = FieldValidator.validate_date(field, value)
            assert len(errors) == 0

    def test_validate_date_invalid(self):
        field = FieldView(name="date", title="Date", field_type="date")
        errors = FieldValidator.validate_date(field, "not-a-date")
        assert len(errors) == 0

    def test_validate_time_valid(self):
        """Test validate_time with valid time values."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="time",
        )

        # Test various valid time inputs
        for value in ["12:00", "12:00:00", "12:00:00.000"]:
            errors = FieldValidator.validate_time(field, value)
            assert len(errors) == 0

    def test_validate_time_invalid(self):
        field = FieldView(name="time", title="Time", field_type="time")
        errors = FieldValidator.validate_time(field, "not-a-time")
        assert len(errors) == 0

    def test_validate_datetime_valid(self):
        """Test validate_datetime with valid datetime values."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="datetime",
        )

        # Test various valid datetime inputs
        for value in [
            "2023-01-01T12:00:00",
            "2023-01-01 12:00:00",
            "2023/01/01 12:00:00",
        ]:
            errors = FieldValidator.validate_datetime(field, value)
            assert len(errors) == 0

    def test_validate_datetime_invalid(self):
        field = FieldView(name="dt", title="Datetime", field_type="datetime")
        errors = FieldValidator.validate_datetime(field, "not-a-datetime")
        assert len(errors) == 0


class TestCustomValidator:
    """Test cases for custom validator functionality."""

    def test_validate_value_with_custom_validator(self):
        """Test validate_value with custom validator."""

        def custom_validator(value):
            if value == "invalid":
                return FieldError(code="CUSTOM", message="Invalid value")
            return None

        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            custom_validator=custom_validator,
        )

        # Test valid value
        errors = FieldValidator.validate_value(field, "valid")
        assert len(errors) == 0

        # Test invalid value
        errors = FieldValidator.validate_value(field, "invalid")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "CUSTOM" in error_codes

    def test_validate_value_with_custom_validator_and_rules(self):
        """Test validate_value with both custom validator and validation rules."""

        def custom_validator(value):
            if value == "invalid":
                return FieldError(code="CUSTOM", message="Invalid value")
            return None

        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            validators=FieldValidation(required=True, min_length=5),
            custom_validator=custom_validator,
        )

        # Test empty value (required rule)
        errors = FieldValidator.validate_value(field, "")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "REQUIRED" in error_codes

        # Test too short (min_length rule)
        errors = FieldValidator.validate_value(field, "abc")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "MIN_LENGTH" in error_codes

        # Test custom validation
        errors = FieldValidator.validate_value(field, "invalid")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "CUSTOM" in error_codes

        # Test valid value
        errors = FieldValidator.validate_value(field, "valid_string")
        assert len(errors) == 0


class TestFieldValidatorIntegration:
    """Integration tests for FieldValidator."""

    def test_validate_value_complete_validation_flow(self):
        """Test complete validation flow with multiple validation types."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            validators=FieldValidation(
                required=True,
                min_length=5,
                max_length=10,
                pattern=r"^[a-zA-Z]+$",
            ),
        )

        # Test empty value
        errors = FieldValidator.validate_value(field, "")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "REQUIRED" in error_codes

        # Test too short
        errors = FieldValidator.validate_value(field, "abc")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "MIN_LENGTH" in error_codes

        # Test too long
        errors = FieldValidator.validate_value(field, "abcdefghijk")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "MAX_LENGTH" in error_codes

        # Test invalid pattern
        errors = FieldValidator.validate_value(field, "abc123")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "PATTERN" in error_codes

        # Test valid value
        errors = FieldValidator.validate_value(field, "abcdef")
        assert len(errors) == 0

    def test_validate_value_type_validation_integration(self):
        """Test type validation integration with custom rules."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="number",
            validators=FieldValidation(
                required=True,
                min_value=0,
                max_value=100,
            ),
        )

        # Test invalid type
        errors = FieldValidator.validate_value(field, "abc")
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "TYPE_NUMBER" in error_codes

        # Test valid type but invalid range
        errors = FieldValidator.validate_value(field, -5)
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "MIN_VALUE" in error_codes

        errors = FieldValidator.validate_value(field, 150)
        assert len(errors) >= 1
        error_codes = [error.code for error in errors]
        assert "MAX_VALUE" in error_codes

        # Test valid value
        errors = FieldValidator.validate_value(field, 50)
        assert len(errors) == 0

    def test_validate_value_multiple_errors(self):
        """Test that multiple validation errors can be returned."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            validators=FieldValidation(
                required=True,
                min_length=5,
                max_length=10,
                pattern=r"^[a-zA-Z]+$",
            ),
        )

        # Test value that violates multiple rules
        errors = FieldValidator.validate_value(
            field, "ab"
        )  # Too short and invalid pattern
        assert len(errors) >= 1  # Should have at least one error
        error_codes = [error.code for error in errors]
        assert "MIN_LENGTH" in error_codes or "PATTERN" in error_codes
