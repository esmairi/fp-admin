"""
Unit tests for base field classes.

This module tests the core field functionality including FieldView, FieldViewKwargs,
and related base classes.
"""

import pytest
from pydantic import ValidationError
from sqlmodel import SQLModel

from fp_admin.admin.fields.base import FieldView, get_default_widget
from fp_admin.admin.fields.errors import FieldError
from fp_admin.admin.fields.field_validator import FieldValidation


class TestGetDefaultWidget:
    """Test cases for get_default_widget function."""

    def test_get_default_widget_string(self):
        """Test getting default widget for string field type."""
        widget = get_default_widget("string")
        assert widget == "text"

    def test_get_default_widget_number(self):
        """Test getting default widget for number field type."""
        widget = get_default_widget("number")
        assert widget == "input"

    def test_get_default_widget_boolean(self):
        """Test getting default widget for boolean field type."""
        widget = get_default_widget("boolean")
        assert widget == "Checkbox"

    def test_get_default_widget_unknown_type(self):
        """Test getting default widget for unknown field type."""
        widget = get_default_widget("unknown_type")
        assert widget == "text"  # Default fallback


class TestFieldView:
    """Test cases for FieldView class."""

    def test_field_view_creation_basic(self):
        """Test creating a basic FieldView."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
        )

        assert field.name == "test_field"
        assert field.title == "Test Field"
        assert field.field_type == "string"
        assert field.widget == "text"  # Default widget
        assert field.required is False
        assert field.readonly is False
        assert field.disabled is False
        assert field.is_primary_key is False

    def test_field_view_creation_with_all_options(self):
        """Test creating FieldView with all options."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            help_text="Help text",
            widget="textarea",
            required=True,
            readonly=True,
            disabled=True,
            placeholder="Enter text",
            default_value="default",
            options={"key": "value"},
            is_primary_key=True,
        )

        assert field.name == "test_field"
        assert field.title == "Test Field"
        assert field.field_type == "string"
        assert field.help_text == "Help text"
        assert field.widget == "textarea"
        assert field.required is True
        assert field.readonly is True
        assert field.disabled is True
        assert field.placeholder == "Enter text"
        assert field.default_value == "default"
        assert field.options == {"key": "value"}
        assert field.is_primary_key is True

    def test_field_view_default_widget_assignment(self):
        """Test that default widget is assigned when not provided."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="number",
        )

        assert field.widget == "input"  # Default for number

    def test_field_view_explicit_none_widget(self):
        """Test that widget can be explicitly set to None."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            widget=None,
        )

        assert field.widget is None

    def test_field_view_validation_creation(self):
        """Test creating FieldView with validation."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            validators=FieldValidation(required=True, min_length=5, max_length=100),
        )

        assert field.validators is not None
        assert field.validators.required is True
        assert field.validators.min_length == 5
        assert field.validators.max_length == 100

    def test_field_view_custom_validator(self):
        """Test creating FieldView with custom validator."""

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

        assert field.custom_validator is not None
        assert field.custom_validator("valid") is None
        assert field.custom_validator("invalid") is not None

    def test_field_view_model_class(self):
        """Test creating FieldView with model class."""

        class TestModel(SQLModel):
            pass

        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            model_class=TestModel,
        )

        assert field.model_class == TestModel

    def test_field_view_validation_method(self):
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            validators=FieldValidation(required=True, min_length=3),
        )
        errors = field.validate_value("")
        error_codes = {e.code for e in errors}
        assert len(errors) == 2
        assert "REQUIRED" in error_codes
        assert "MIN_LENGTH" in error_codes

    def test_field_view_validation_with_custom_validator(self):
        """Test FieldView validation with custom validator."""

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
        errors = field.validate_value("valid")
        assert len(errors) == 0

        # Test invalid value
        errors = field.validate_value("invalid")
        assert len(errors) == 1
        assert errors[0].code == "CUSTOM"

    def test_field_view_serialization(self):
        """Test FieldView serialization to dict."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
            help_text="Help text",
            widget="textarea",
            required=True,
            readonly=True,
            disabled=True,
            placeholder="Enter text",
            default_value="default",
            options={"key": "value"},
            is_primary_key=True,
        )

        field_dict = field.model_dump()

        assert field_dict["name"] == "test_field"
        assert field_dict["title"] == "Test Field"
        assert field_dict["field_type"] == "string"
        assert field_dict["help_text"] == "Help text"
        assert field_dict["widget"] == "textarea"
        assert field_dict["required"] is True
        assert field_dict["readonly"] is True
        assert field_dict["disabled"] is True
        assert field_dict["placeholder"] == "Enter text"
        assert field_dict["default_value"] == "default"
        assert field_dict["options"] == {"key": "value"}
        assert field_dict["is_primary_key"] is True

    def test_field_view_from_dict(self):
        """Test creating FieldView from dictionary."""
        field_data = {
            "name": "test_field",
            "title": "Test Field",
            "field_type": "string",
            "help_text": "Help text",
            "widget": "textarea",
            "required": True,
        }

        field = FieldView(**field_data)

        assert field.name == "test_field"
        assert field.title == "Test Field"
        assert field.field_type == "string"
        assert field.help_text == "Help text"
        assert field.widget == "textarea"
        assert field.required is True

    def test_field_view_invalid_field_type(self):
        """Test FieldView with invalid field type."""
        with pytest.raises(ValidationError):
            FieldView(
                name="test_field",
                title="Test Field",
                field_type="invalid_type",  # type: ignore
            )

    def test_field_view_optional_fields_defaults(self):
        """Test that optional fields have correct defaults."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="string",
        )

        assert field.title == "Test Field"
        assert field.help_text is None
        assert field.widget == "text"  # Default widget
        assert field.widget_config is None
        assert field.required is False
        assert field.readonly is False
        assert field.disabled is False
        assert field.placeholder is None
        assert field.default_value is None
        assert field.options is None
        assert field.error is None
        assert field.validators is not None  # Default FieldValidation
        assert field.custom_validator is None
        assert field.is_primary_key is False
        assert field.model_class is None
