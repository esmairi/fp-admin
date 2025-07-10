"""
Unit tests for field factory.

This module tests the FieldFactory class and its methods
for creating different field types.
"""

from fp_admin.admin.fields.base import FieldView
from fp_admin.admin.fields.errors import FieldError
from fp_admin.admin.fields.field_factory import FieldFactory
from fp_admin.admin.fields.widgets import WidgetConfig


class TestFieldFactory:
    """Test cases for FieldFactory class."""

    def test_get_validator_basic(self):
        """Test get_validator with basic validation parameters."""
        validation = FieldFactory.get_validator(
            required=True,
            min_length=5,
            max_length=100,
        )

        assert validation is not None
        assert validation.required is True
        assert validation.min_length == 5
        assert validation.max_length == 100

    def test_get_validator_no_validation_params(self):
        """Test get_validator with no validation parameters."""
        validation = FieldFactory.get_validator(
            name="test_field",
            title="Test Field",
            widget="text",
        )

        assert validation is None

    def test_get_validator_all_validation_params(self):
        """Test get_validator with all validation parameters."""
        validation = FieldFactory.get_validator(
            required=True,
            min_length=5,
            max_length=100,
            min_value=0,
            max_value=1000,
            pattern=r"^[a-zA-Z]+$",
        )

        assert validation is not None
        assert validation.required is True
        assert validation.min_length == 5
        assert validation.max_length == 100
        assert validation.min_value == 0
        assert validation.max_value == 1000
        assert validation.pattern == r"^[a-zA-Z]+$"

    def test_filter_field_kwargs(self):
        """Test _filter_field_kwargs method."""
        kwargs = {
            "name": "test_field",
            "title": "Test Field",
            "required": True,
            "min_length": 5,
            "max_length": 100,
            "widget": "text",
            "help_text": "Help text",
        }

        filtered_kwargs = FieldFactory._filter_field_kwargs(**kwargs)

        # Validation parameters should be filtered out
        assert "required" not in filtered_kwargs
        assert "min_length" not in filtered_kwargs
        assert "max_length" not in filtered_kwargs

        # Field parameters should remain
        assert filtered_kwargs["name"] == "test_field"
        assert filtered_kwargs["title"] == "Test Field"
        assert filtered_kwargs["widget"] == "text"
        assert filtered_kwargs["help_text"] == "Help text"

    def test_get_custom_validator(self):
        """Test _get_custom_validator method."""

        def custom_validator(value):
            if value == "invalid":
                return FieldError(code="CUSTOM", message="Invalid value")
            return None

        validator = FieldFactory._get_custom_validator(
            custom_validator=custom_validator
        )

        assert validator is not None
        assert validator("valid") is None
        assert validator("invalid") is not None

    def test_get_custom_validator_none(self):
        """Test _get_custom_validator with no custom validator."""
        validator = FieldFactory._get_custom_validator()

        assert validator is None


class TestStringFields:
    """Test cases for string field factory methods."""

    def test_string_field_basic(self):
        """Test string_field with basic parameters."""
        field = FieldFactory.string_field("test_field", "Test Field")

        assert field.name == "test_field"
        assert field.title == "Test Field"
        assert field.field_type == "string"
        assert field.widget == "text"  # Default widget

    def test_string_field_with_validation(self):
        """Test string_field with validation parameters."""
        field = FieldFactory.string_field(
            "test_field",
            "Test Field",
            required=True,
            min_length=5,
            max_length=100,
        )

        assert field.name == "test_field"
        assert field.title == "Test Field"
        assert field.field_type == "string"
        assert field.validators is not None
        assert field.validators.required is True
        assert field.validators.min_length == 5
        assert field.validators.max_length == 100

    def test_string_field_with_custom_validator(self):
        """Test string_field with custom validator."""

        def custom_validator(value):
            if value == "invalid":
                return FieldError(code="CUSTOM", message="Invalid value")
            return None

        field = FieldFactory.string_field(
            "test_field",
            "Test Field",
            custom_validator=custom_validator,
        )

        assert field.custom_validator is not None
        assert field.custom_validator("valid") is None
        assert field.custom_validator("invalid") is not None

    def test_text_field_alias(self):
        """Test text_field as alias for string_field."""
        field = FieldFactory.text_field("test_field", "Test Field")

        assert field.name == "test_field"
        assert field.title == "Test Field"
        assert field.field_type == "string"
        assert field.widget == "text"

    def test_email_field(self):
        """Test email_field with email validation."""
        field = FieldFactory.email_field("email", "Email")

        assert field.name == "email"
        assert field.title == "Email"
        assert field.field_type == "string"
        assert field.validators is not None
        assert (
            field.validators.pattern
            == r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )

    def test_email_field_with_additional_validation(self):
        """Test email_field with additional validation."""
        field = FieldFactory.email_field(
            "email",
            "Email",
            required=True,
            min_length=10,
        )

        assert field.validators is not None
        assert field.validators.required is True
        assert field.validators.min_length == 10
        assert (
            field.validators.pattern
            == r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )

    def test_password_field(self):
        """Test password_field."""
        field = FieldFactory.password_field("password", "Password")

        assert field.name == "password"
        assert field.title == "Password"
        assert field.field_type == "string"
        assert field.widget == "password"

    def test_textarea_field(self):
        """Test textarea_field."""
        field = FieldFactory.textarea_field("description", "Description")

        assert field.name == "description"
        assert field.title == "Description"
        assert field.field_type == "string"
        assert field.widget == "textarea"


class TestNumberFields:
    """Test cases for number field factory methods."""

    def test_number_field_basic(self):
        """Test number_field with basic parameters."""
        field = FieldFactory.number_field("age", "Age")

        assert field.name == "age"
        assert field.title == "Age"
        assert field.field_type == "number"

    def test_number_field_with_validation(self):
        """Test number_field with validation parameters."""
        field = FieldFactory.number_field(
            "age",
            "Age",
            required=True,
            min_value=0,
            max_value=120,
        )

        assert field.name == "age"
        assert field.title == "Age"
        assert field.field_type == "number"
        assert field.validators is not None
        assert field.validators.required is True
        assert field.validators.min_value == 0
        assert field.validators.max_value == 120

    def test_float_field(self):
        """Test float_field."""
        field = FieldFactory.float_field("price", "Price")

        assert field.name == "price"
        assert field.title == "Price"
        assert field.field_type == "float"

    def test_slider_field(self):
        """Test slider_field."""
        field = FieldFactory.slider_field("rating", "Rating")

        assert field.name == "rating"
        assert field.title == "Rating"
        assert field.field_type == "number"
        assert field.widget == "Slider"


class TestDateTimeFields:
    """Test cases for date/time field factory methods."""

    def test_time_field(self):
        """Test time_field."""
        field = FieldFactory.time_field("start_time", "Start Time")

        assert field.name == "start_time"
        assert field.title == "Start Time"
        assert field.field_type == "time"
        assert field.widget == "calendar"

    def test_time_field_with_config(self):
        """Test time_field with widget configuration."""
        field = FieldFactory.time_field(
            "start_time",
            "Start Time",
            widget_config=WidgetConfig(timeOnly=True),
        )

        assert field.name == "start_time"
        assert field.title == "Start Time"
        assert field.field_type == "time"
        assert field.widget_config is not None
        assert field.widget_config.timeOnly is True

    def test_datetime_field(self):
        """Test datetime_field."""
        field = FieldFactory.datetime_field("created_at", "Created At")

        assert field.name == "created_at"
        assert field.title == "Created At"
        assert field.field_type == "datetime"
        assert field.widget == "calendar"

    def test_datetime_field_with_config(self):
        """Test datetime_field with widget configuration."""
        field = FieldFactory.datetime_field(
            "created_at",
            "Created At",
            widget_config=WidgetConfig(showTime=True),
        )

        assert field.name == "created_at"
        assert field.title == "Created At"
        assert field.field_type == "datetime"
        assert field.widget_config is not None
        assert field.widget_config.showTime is True

    def test_date_field(self):
        """Test date_field."""
        field = FieldFactory.date_field("birth_date", "Birth Date")

        assert field.name == "birth_date"
        assert field.title == "Birth Date"
        assert field.field_type == "date"
        assert field.widget == "calendar"


class TestBooleanFields:
    """Test cases for boolean field factory methods."""

    def test_boolean_field(self):
        """Test boolean_field."""
        field = FieldFactory.boolean_field("active", "Active")

        assert field.name == "active"
        assert field.title == "Active"
        assert field.field_type == "boolean"
        assert field.widget == "Checkbox"

    def test_checkbox_field(self):
        """Test checkbox_field."""
        field = FieldFactory.checkbox_field("terms", "Accept Terms")

        assert field.name == "terms"
        assert field.title == "Accept Terms"
        assert field.field_type == "boolean"
        assert field.widget == "Checkbox"

    def test_switch_field(self):
        """Test switch_field."""
        field = FieldFactory.switch_field("notifications", "Enable Notifications")

        assert field.name == "notifications"
        assert field.title == "Enable Notifications"
        assert field.field_type == "boolean"
        assert field.widget == "switch"


class TestChoiceFields:
    """Test cases for choice field factory methods."""

    def test_choice_field(self):
        """Test choice_field."""
        field = FieldFactory.choice_field("status", "Status")

        assert field.name == "status"
        assert field.title == "Status"
        assert field.field_type == "choice"
        assert field.widget == "dropdown"

    def test_choice_field_with_options(self):
        """Test choice_field with options."""
        options = {"active": "Active", "inactive": "Inactive", "pending": "Pending"}
        field = FieldFactory.choice_field(
            "status",
            "Status",
            options=options,
        )

        assert field.name == "status"
        assert field.title == "Status"
        assert field.field_type == "choice"
        assert field.options == options

    def test_multichoice_field(self):
        """Test multichoice_field."""
        field = FieldFactory.multichoice_field("tags", "Tags")

        assert field.name == "tags"
        assert field.title == "Tags"
        assert field.field_type == "multichoice"
        assert field.widget == "multiSelect"

    def test_multichoice_field_with_options(self):
        """Test multichoice_field with options."""
        options = {"tech": "Technology", "design": "Design", "marketing": "Marketing"}
        field = FieldFactory.multichoice_field(
            "tags",
            "Tags",
            options=options,
        )

        assert field.name == "tags"
        assert field.title == "Tags"
        assert field.field_type == "multichoice"
        assert field.options == options


class TestRelationshipFields:
    """Test cases for relationship field factory methods."""

    def test_foreignkey_field(self):
        """Test foreignkey_field."""
        field = FieldFactory.foreignkey_field("category", "Category")

        assert field.name == "category"
        assert field.title == "Category"
        assert field.field_type == "foreignkey"
        assert field.widget == "dropdown"

    def test_many_to_many_field(self):
        """Test many_to_many_field."""
        field = FieldFactory.many_to_many_field("tags", "Tags")

        assert field.name == "tags"
        assert field.title == "Tags"
        assert field.field_type == "many_to_many"
        assert field.widget == "autoComplete"

    def test_onetoone_field(self):
        """Test onetoone_field."""
        field = FieldFactory.onetoone_field("profile", "Profile")

        assert field.name == "profile"
        assert field.title == "Profile"
        assert field.field_type == "OneToOneField"
        assert field.widget == "dropdown"


class TestFileFields:
    """Test cases for file field factory methods."""

    def test_file_field(self):
        """Test file_field."""
        field = FieldFactory.file_field("document", "Document")

        assert field.name == "document"
        assert field.title == "Document"
        assert field.field_type == "file"
        assert field.widget == "upload"

    def test_file_field_with_accept(self):
        """Test file_field with accept parameter."""
        field = FieldFactory.file_field(
            "document",
            "Document",
            widget_config=WidgetConfig(accept=".pdf,.doc,.docx"),
        )

        assert field.name == "document"
        assert field.title == "Document"
        assert field.field_type == "file"
        assert field.widget == "upload"
        assert field.widget_config is not None
        assert field.widget_config.accept == ".pdf,.doc,.docx"

    def test_image_field(self):
        """Test image_field."""
        field = FieldFactory.image_field("avatar", "Avatar")

        assert field.name == "avatar"
        assert field.title == "Avatar"
        assert field.field_type == "image"
        assert field.widget == "image"

    def test_image_field_with_preview(self):
        """Test image_field with preview configuration."""
        field = FieldFactory.image_field(
            "avatar",
            "Avatar",
            widget_config=WidgetConfig(preview=True, accept="image/*"),
        )

        assert field.name == "avatar"
        assert field.title == "Avatar"
        assert field.field_type == "image"
        assert field.widget == "image"
        assert field.widget_config is not None
        assert field.widget_config.preview is True
        assert field.widget_config.accept == "image/*"


class TestSpecialFields:
    """Test cases for special field factory methods."""

    def test_json_field(self):
        """Test json_field."""
        field = FieldFactory.json_field("config", "Configuration")

        assert field.name == "config"
        assert field.title == "Configuration"
        assert field.field_type == "json"
        assert field.widget == "editor"

    def test_json_field_with_editor_type(self):
        """Test json_field with custom editor type."""
        field = FieldFactory.json_field(
            "config",
            "Configuration",
            widget_config=WidgetConfig(editor_type="ace"),
        )

        assert field.name == "config"
        assert field.title == "Configuration"
        assert field.field_type == "json"
        assert field.widget == "editor"
        assert field.widget_config is not None
        assert field.widget_config.editor_type == "ace"

    def test_color_field(self):
        """Test color_field."""
        field = FieldFactory.color_field("theme_color", "Theme Color")

        assert field.name == "theme_color"
        assert field.title == "Theme Color"
        assert field.field_type == "color"
        assert field.widget == "colorPicker"

    def test_primarykey_field(self):
        """Test primarykey_field."""
        field = FieldFactory.primarykey_field("id", "ID")

        assert field.name == "id"
        assert field.title == "ID"
        assert field.field_type == "primarykey"
        assert field.is_primary_key is True


class TestWidgetSpecificFields:
    """Test cases for widget-specific field factory methods."""

    def test_select_field(self):
        """Test select_field."""
        field = FieldFactory.select_field("status", "Status")

        assert field.name == "status"
        assert field.title == "Status"
        assert field.field_type == "choice"
        assert field.widget == "select"

    def test_radio_field(self):
        """Test radio_field."""
        field = FieldFactory.radio_field("gender", "Gender")

        assert field.name == "gender"
        assert field.title == "Gender"
        assert field.field_type == "choice"
        assert field.widget == "radio"

    def test_checkbox_group_field(self):
        """Test checkbox_group_field."""
        field = FieldFactory.checkbox_group_field("interests", "Interests")

        assert field.name == "interests"
        assert field.title == "Interests"
        assert field.field_type == "multichoice"
        assert field.widget == "multiSelect"

    def test_autocomplete_field(self):
        field = FieldFactory.autocomplete_field("tags", "Tags")
        assert field.field_type == "string"
        assert field.widget == "autoComplete"

    def test_toggle_field(self):
        """Test toggle_field."""
        field = FieldFactory.toggle_field("notifications", "Notifications")

        assert field.name == "notifications"
        assert field.title == "Notifications"
        assert field.field_type == "boolean"
        assert field.widget == "switch"

    def test_chips_field(self):
        """Test chips_field."""
        field = FieldFactory.chips_field("tags", "Tags")

        assert field.name == "tags"
        assert field.title == "Tags"
        assert field.field_type == "multichoice"
        assert field.widget == "chips"

    def test_listbox_field(self):
        """Test listbox_field."""
        field = FieldFactory.listbox_field("categories", "Categories")

        assert field.name == "categories"
        assert field.title == "Categories"
        assert field.field_type == "multichoice"
        assert field.widget == "listBox"

    def test_selectbutton_field(self):
        field = FieldFactory.selectbutton_field("status", "Status")
        assert field.widget == "dropdown"

    def test_code_editor_field(self):
        """Test code_editor_field."""
        field = FieldFactory.code_editor_field("code", "Code")

        assert field.name == "code"
        assert field.title == "Code"
        assert field.field_type == "json"
        assert field.widget == "editor"

    def test_color_picker_field(self):
        """Test color_picker_field."""
        field = FieldFactory.color_picker_field("color", "Color")

        assert field.name == "color"
        assert field.title == "Color"
        assert field.field_type == "color"
        assert field.widget == "colorPicker"

    def test_richtext_field(self):
        """Test richtext_field."""
        field = FieldFactory.richtext_field("content", "Content")

        assert field.name == "content"
        assert field.title == "Content"
        assert field.field_type == "string"
        assert field.widget == "textarea"

    def test_markdown_field(self):
        """Test markdown_field."""
        field = FieldFactory.markdown_field("content", "Content")

        assert field.name == "content"
        assert field.title == "Content"
        assert field.field_type == "string"
        assert field.widget == "textarea"


class TestFieldFactoryIntegration:
    """Integration tests for FieldFactory."""

    def test_field_factory_creates_valid_fields(self):
        """Test that FieldFactory creates valid FieldView instances."""
        field_types = [
            ("string", FieldFactory.string_field),
            ("number", FieldFactory.number_field),
            ("boolean", FieldFactory.boolean_field),
            ("choice", FieldFactory.choice_field),
            ("multichoice", FieldFactory.multichoice_field),
        ]

        for field_type, factory_method in field_types:
            field = factory_method("test_field", "Test Field")

            assert isinstance(field, FieldView)
            assert field.name == "test_field"
            assert field.title == "Test Field"
            assert field.field_type == field_type

    def test_field_factory_validation_integration(self):
        field = FieldFactory.string_field(
            "test_field", "Test Field", required=True, min_length=5
        )
        errors = field.validate_value("")
        error_codes = {e.code for e in errors}
        assert len(errors) == 2
        assert "REQUIRED" in error_codes
        assert "MIN_LENGTH" in error_codes

    def test_field_factory_custom_validator_integration(self):
        """Test FieldFactory with custom validator integration."""

        def custom_validator(value):
            if value == "invalid":
                return FieldError(code="CUSTOM", message="Invalid value")
            return None

        field = FieldFactory.string_field(
            "test_field",
            "Test Field",
            custom_validator=custom_validator,
        )

        # Test custom validation
        errors = field.validate_value("valid")
        assert len(errors) == 0

        errors = field.validate_value("invalid")
        assert len(errors) == 1
        assert errors[0].code == "CUSTOM"
