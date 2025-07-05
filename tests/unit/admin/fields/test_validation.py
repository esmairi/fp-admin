"""
Unit tests for field validation.

Tests the FieldValidation class and validation rules.
"""

import pytest

from fp_admin.admin.fields.validation import FieldValidation

pytestmark = pytest.mark.unit


class TestFieldValidation:
    """Test cases for FieldValidation."""

    def test_default_validation(self) -> None:
        """Test that FieldValidation has correct default values."""
        validation = FieldValidation()

        assert validation.required is False
        assert validation.min_length is None
        assert validation.max_length is None
        assert validation.min_value is None
        assert validation.max_value is None
        assert validation.pattern is None

    def test_required_validation(self) -> None:
        """Test required field validation."""
        validation = FieldValidation(required=True)
        assert validation.required is True

    def test_length_validation(self) -> None:
        """Test length validation rules."""
        validation = FieldValidation(min_length=3, max_length=10)

        assert validation.min_length == 3
        assert validation.max_length == 10

    def test_value_validation(self) -> None:
        """Test value validation rules."""
        validation = FieldValidation(min_value=0, max_value=100)

        assert validation.min_value == 0
        assert validation.max_value == 100

    def test_pattern_validation(self) -> None:
        """Test pattern validation rule."""
        pattern = r"^[a-zA-Z]+$"
        validation = FieldValidation(pattern=pattern)

        assert validation.pattern == pattern

    def test_float_values(self) -> None:
        """Test that float values are accepted for min/max_value."""
        validation = FieldValidation(min_value=0.5, max_value=99.9)

        assert validation.min_value == 0.5
        assert validation.max_value == 99.9

    def test_negative_values(self) -> None:
        """Test that negative values are accepted."""
        validation = FieldValidation(min_value=-100, max_value=-1)

        assert validation.min_value == -100
        assert validation.max_value == -1

    def test_zero_values(self) -> None:
        """Test that zero values are accepted."""
        validation = FieldValidation(min_value=0, max_value=0)

        assert validation.min_value == 0
        assert validation.max_value == 0

    def test_complex_validation(self) -> None:
        """Test complex validation with multiple rules."""
        validation = FieldValidation(
            required=True,
            min_length=5,
            max_length=50,
            min_value=1,
            max_value=1000,
            pattern=r"^[a-zA-Z0-9_]+$",
        )

        assert validation.required is True
        assert validation.min_length == 5
        assert validation.max_length == 50
        assert validation.min_value == 1
        assert validation.max_value == 1000
        assert validation.pattern == r"^[a-zA-Z0-9_]+$"

    def test_validation_serialization(self) -> None:
        """Test that validation can be serialized to dict."""
        validation = FieldValidation(
            required=True, min_length=3, max_length=10, pattern=r"^[a-z]+$"
        )

        data = validation.model_dump()

        assert data["required"] is True
        assert data["min_length"] == 3
        assert data["max_length"] == 10
        assert data["pattern"] == r"^[a-z]+$"
        assert data["min_value"] is None
        assert data["max_value"] is None

    def test_validation_from_dict(self) -> None:
        """Test that validation can be created from dict."""
        data = {
            "required": True,
            "min_length": 5,
            "max_length": 20,
            "min_value": 1,
            "max_value": 100,
            "pattern": r"^[A-Z]+$",
        }

        validation = FieldValidation(**data)

        assert validation.required is True
        assert validation.min_length == 5
        assert validation.max_length == 20
        assert validation.min_value == 1
        assert validation.max_value == 100
        assert validation.pattern == r"^[A-Z]+$"
