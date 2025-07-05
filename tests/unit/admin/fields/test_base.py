"""
Unit tests for base field classes.

Tests the FieldView class and its factory methods.
"""

import pytest
from pydantic import ValidationError

from fp_admin.admin.fields.base import FieldView
from fp_admin.admin.fields.validation import FieldValidation
from fp_admin.admin.fields.widgets import DEFAULT_WIDGETS

pytestmark = pytest.mark.unit


class TestFieldView:
    """Test cases for FieldView."""

    def test_field_view_creation(self) -> None:
        """Test basic FieldView creation."""
        field = FieldView(name="test_field", title="Test Field", field_type="text")

        assert field.name == "test_field"
        assert field.title == "Test Field"
        assert field.field_type == "text"
        assert field.required is False
        assert field.readonly is False
        assert field.disabled is False
        assert field.widget == "text"  # Default widget

    def test_field_view_required_fields(self) -> None:
        """Test that name, title, and field_type are required fields."""
        field = FieldView(
            name="required_test", title="Required Test", field_type="number"
        )

        assert field.name == "required_test"
        assert field.title == "Required Test"
        assert field.field_type == "number"
        assert field.widget == "number"  # Default widget

    def test_field_view_missing_name(self) -> None:
        """Test that name field is required."""
        with pytest.raises(ValidationError):
            FieldView(title="Test", field_type="text")

    def test_field_view_missing_field_type(self) -> None:
        """Test that field_type field is required."""
        with pytest.raises(ValidationError):
            FieldView(name="test", title="Test")

    def test_field_view_optional_fields(self) -> None:
        """Test that optional fields work correctly."""
        field = FieldView(
            name="test",
            title="Test",
            field_type="text",
            widget="email",  # Custom widget
            help_text="Help text",
            placeholder="Enter value",
            required=True,
            readonly=True,
            disabled=True,
            default_value="default",
        )

        assert field.widget == "email"
        assert field.help_text == "Help text"
        assert field.placeholder == "Enter value"
        assert field.required is True
        assert field.readonly is True
        assert field.disabled is True
        assert field.default_value == "default"

    def test_field_view_validation_field(self) -> None:
        """Test that validation field works correctly."""
        validation = FieldValidation(required=True, min_length=3)
        field = FieldView(
            name="test", title="Test", field_type="text", validation=validation
        )

        assert field.validation is not None
        assert field.validation.required is True
        assert field.validation.min_length == 3


class TestFieldViewWidgets:
    """Test cases for FieldView widget functionality."""

    def test_default_widget_assignment(self) -> None:
        """Test that default widgets are assigned correctly."""
        # Test all field types have default widgets
        field_types = [
            "text",
            "number",
            "date",
            "checkbox",
            "radio",
            "select",
            "textarea",
            "file",
            "relationship",
        ]

        for field_type in field_types:
            field = FieldView(
                name=f"test_{field_type}",
                title=f"Test {field_type}",
                field_type=field_type,
            )

            if field_type in DEFAULT_WIDGETS:
                assert field.widget == DEFAULT_WIDGETS[field_type]
            else:
                assert field.widget == "text"  # Fallback default

    def test_custom_widget_assignment(self) -> None:
        """Test that custom widgets can be assigned."""
        field = FieldView(
            name="custom_field",
            title="Custom Field",
            field_type="text",
            widget="search",
        )

        assert field.widget == "search"
        assert field.field_type == "text"

    def test_widget_specific_factory_methods(self) -> None:
        """Test widget-specific factory methods."""
        # Test toggle field
        toggle_field = FieldView.toggle_field(name="toggle", title="Toggle Switch")
        assert toggle_field.widget == "toggle"
        assert toggle_field.field_type == "checkbox"

        # Test switch field
        switch_field = FieldView.switch_field(name="switch", title="Switch")
        assert switch_field.widget == "switch"
        assert switch_field.field_type == "checkbox"

        # Test range field
        range_field = FieldView.range_field(name="range", title="Range Slider")
        assert range_field.widget == "range"
        assert range_field.field_type == "number"

        # Test slider field
        slider_field = FieldView.slider_field(name="slider", title="Slider")
        assert slider_field.widget == "slider"
        assert slider_field.field_type == "number"

        # Test richtext field
        richtext_field = FieldView.richtext_field(name="richtext", title="Rich Text")
        assert richtext_field.widget == "richtext"
        assert richtext_field.field_type == "textarea"

        # Test markdown field
        markdown_field = FieldView.markdown_field(name="markdown", title="Markdown")
        assert markdown_field.widget == "markdown"
        assert markdown_field.field_type == "textarea"

    def test_widget_with_validation(self) -> None:
        """Test that widgets work with validation."""
        field = FieldView.toggle_field(
            name="toggle", title="Toggle", validation=FieldValidation(required=True)
        )

        assert field.widget == "toggle"
        assert field.field_type == "checkbox"
        assert field.validation is not None
        assert field.validation.required is True

    def test_widget_serialization(self) -> None:
        """Test that widgets are properly serialized."""
        field = FieldView.range_field(
            name="range", title="Range", min_selections=1, max_selections=10
        )

        data = field.model_dump()
        assert data["widget"] == "range"
        assert data["field_type"] == "number"


class TestFieldViewFactoryMethods:
    """Test cases for FieldView factory methods."""

    def test_text_field_factory(self) -> None:
        """Test text_field factory method."""
        field = FieldView.text_field(
            name="username",
            title="Username",
            required=True,
            placeholder="Enter username",
        )

        assert field.name == "username"
        assert field.title == "Username"
        assert field.field_type == "text"
        assert field.required is True
        assert field.placeholder == "Enter username"

    def test_email_field_factory(self) -> None:
        """Test email_field factory method."""
        field = FieldView.email_field(
            name="email", title="Email Address", required=True
        )

        assert field.name == "email"
        assert field.title == "Email Address"
        assert field.field_type == "text"
        assert field.required is True
        assert field.validation is not None
        assert field.validation.pattern is not None

    def test_password_field_factory(self) -> None:
        """Test password_field factory method."""
        field = FieldView.password_field(
            name="password", title="Password", required=True
        )

        assert field.name == "password"
        assert field.title == "Password"
        assert field.field_type == "text"
        assert field.required is True

    def test_number_field_factory(self) -> None:
        """Test number_field factory method."""
        field = FieldView.number_field(name="age", title="Age", required=True)

        assert field.name == "age"
        assert field.title == "Age"
        assert field.field_type == "number"
        assert field.required is True

    def test_date_field_factory(self) -> None:
        """Test date_field factory method."""
        field = FieldView.date_field(name="birth_date", title="Birth Date")

        assert field.name == "birth_date"
        assert field.title == "Birth Date"
        assert field.field_type == "date"

    def test_checkbox_field_factory(self) -> None:
        """Test checkbox_field factory method."""
        field = FieldView.checkbox_field(
            name="newsletter", title="Subscribe to Newsletter", default_value=True
        )

        assert field.name == "newsletter"
        assert field.title == "Subscribe to Newsletter"
        assert field.field_type == "checkbox"
        assert field.default_value is True

    def test_textarea_field_factory(self) -> None:
        """Test textarea_field factory method."""
        field = FieldView.textarea_field(
            name="bio", title="Biography", placeholder="Tell us about yourself"
        )

        assert field.name == "bio"
        assert field.title == "Biography"
        assert field.field_type == "textarea"
        assert field.placeholder == "Tell us about yourself"

    def test_file_field_factory(self) -> None:
        """Test file_field factory method."""
        field = FieldView.file_field(name="avatar", title="Profile Picture")

        assert field.name == "avatar"
        assert field.title == "Profile Picture"
        assert field.field_type == "file"


class TestFieldViewValidation:
    """Test cases for FieldView validation methods."""

    def test_validate_value_required_field_empty(self) -> None:
        """Test validation of required field with empty value."""
        field = FieldView(name="test", title="Test", field_type="text", required=True)

        errors = field.validate_value("")
        assert len(errors) == 1
        assert "required" in errors[0].lower()

    def test_validate_value_required_field_none(self) -> None:
        """Test validation of required field with None value."""
        field = FieldView(name="test", title="Test", field_type="text", required=True)

        errors = field.validate_value(None)
        assert len(errors) == 1
        assert "required" in errors[0].lower()

    def test_validate_value_optional_field_empty(self) -> None:
        """Test validation of optional field with empty value."""
        field = FieldView(name="test", title="Test", field_type="text", required=False)

        errors = field.validate_value("")
        assert len(errors) == 0

    def test_validate_value_min_length(self) -> None:
        """Test validation with min_length rule."""
        validation = FieldValidation(min_length=3)
        field = FieldView(
            name="test", title="Test", field_type="text", validation=validation
        )

        # Test valid value
        errors = field.validate_value("abc")
        assert len(errors) == 0

        # Test invalid value
        errors = field.validate_value("ab")
        assert len(errors) == 1
        assert "minimum length" in errors[0].lower()

    def test_validate_value_max_length(self) -> None:
        """Test validation with max_length rule."""
        validation = FieldValidation(max_length=5)
        field = FieldView(
            name="test", title="Test", field_type="text", validation=validation
        )

        # Test valid value
        errors = field.validate_value("abc")
        assert len(errors) == 0

        # Test invalid value
        errors = field.validate_value("abcdef")
        assert len(errors) == 1
        assert "maximum length" in errors[0].lower()

    def test_validate_value_min_value(self) -> None:
        """Test validation with min_value rule."""
        validation = FieldValidation(min_value=0)
        field = FieldView(
            name="test", title="Test", field_type="number", validation=validation
        )

        # Test valid value
        errors = field.validate_value(5)
        assert len(errors) == 0

        # Test invalid value
        errors = field.validate_value(-1)
        assert len(errors) == 1
        assert "minimum value" in errors[0].lower()

    def test_validate_value_max_value(self) -> None:
        """Test validation with max_value rule."""
        validation = FieldValidation(max_value=100)
        field = FieldView(
            name="test", title="Test", field_type="number", validation=validation
        )

        # Test valid value
        errors = field.validate_value(50)
        assert len(errors) == 0

        # Test invalid value
        errors = field.validate_value(150)
        assert len(errors) == 1
        assert "maximum value" in errors[0].lower()

    def test_validate_value_pattern(self) -> None:
        """Test validation with pattern rule."""
        validation = FieldValidation(pattern=r"^[a-zA-Z]+$")
        field = FieldView(
            name="test", title="Test", field_type="text", validation=validation
        )

        # Test valid value
        errors = field.validate_value("abc")
        assert len(errors) == 0

        # Test invalid value
        errors = field.validate_value("abc123")
        assert len(errors) == 1
        assert "invalid format" in errors[0].lower()

    def test_validate_value_multiple_rules(self) -> None:
        """Test validation with multiple rules."""
        validation = FieldValidation(min_length=3, max_length=10, pattern=r"^[a-z]+$")
        field = FieldView(
            name="test", title="Test", field_type="text", validation=validation
        )

        # Test valid value
        errors = field.validate_value("abcde")
        assert len(errors) == 0

        # Test invalid value (too short)
        errors = field.validate_value("ab")
        assert len(errors) == 1
        assert "minimum length" in errors[0].lower()

        # Test invalid value (too long)
        errors = field.validate_value("abcdefghijk")
        assert len(errors) == 1
        assert "maximum length" in errors[0].lower()

        # Test invalid value (wrong pattern)
        errors = field.validate_value("ABC123")
        assert len(errors) == 1
        assert "invalid format" in errors[0].lower()

    def test_validate_value_email_pattern(self) -> None:
        """Test email validation pattern."""
        field = FieldView.email_field("email", "Email")

        # Test valid emails
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
        ]

        for email in valid_emails:
            errors = field.validate_value(email)
            assert len(errors) == 0, f"Email {email} should be valid"

        # Test invalid emails
        invalid_emails = ["invalid-email", "@example.com", "user@", "user@.com"]

        for email in invalid_emails:
            errors = field.validate_value(email)
            assert len(errors) > 0, f"Email {email} should be invalid"


class TestFieldViewSerialization:
    """Test cases for FieldView serialization."""

    def test_field_view_serialization(self) -> None:
        """Test that FieldView can be serialized to dict."""
        field = FieldView(
            name="test_field",
            title="Test Field",
            field_type="text",
            required=True,
            help_text="Help text",
            placeholder="Enter value",
            default_value="default",
        )

        data = field.model_dump()

        assert data["name"] == "test_field"
        assert data["title"] == "Test Field"
        assert data["field_type"] == "text"
        assert data["required"] is True
        assert data["help_text"] == "Help text"
        assert data["placeholder"] == "Enter value"
        assert data["default_value"] == "default"

    def test_field_view_from_dict(self) -> None:
        """Test that FieldView can be created from dict."""
        data = {
            "name": "test_field",
            "title": "Test Field",
            "field_type": "number",
            "required": True,
            "help_text": "Help text",
        }

        field = FieldView(**data)

        assert field.name == "test_field"
        assert field.title == "Test Field"
        assert field.field_type == "number"
        assert field.required is True
        assert field.help_text == "Help text"
