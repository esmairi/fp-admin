"""
Integration tests for the fields package.

Tests that all field components work together correctly.
"""

import pytest

from fp_admin.admin.fields import (
    DEFAULT_WIDGETS,
    ChoicesField,
    FieldChoices,
    FieldError,
    FieldType,
    FieldValidation,
    FieldView,
    MultiChoicesField,
    RelationshipField,
    WidgetType,
)

pytestmark = pytest.mark.unit


class TestFieldsPackageIntegration:
    """Integration tests for the fields package."""

    def test_package_imports(self) -> None:
        """Test that all field classes can be imported from the package."""
        # This test ensures that the __init__.py file exports everything correctly
        assert FieldType is not None
        assert FieldValidation is not None
        assert FieldChoices is not None
        assert FieldError is not None
        assert FieldView is not None
        assert ChoicesField is not None
        assert MultiChoicesField is not None
        assert RelationshipField is not None
        assert WidgetType is not None
        assert DEFAULT_WIDGETS is not None

    def test_field_view_with_validation(self) -> None:
        """Test FieldView with validation rules."""
        validation = FieldValidation(
            required=True, min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$"
        )

        field = FieldView(
            name="username",
            title="Username",
            field_type="text",
            validation=validation,
            help_text="Choose a unique username",
        )

        assert field.name == "username"
        assert field.title == "Username"
        assert field.field_type == "text"
        assert field.validation is not None
        assert field.validation.required is True
        assert field.validation.min_length == 3
        assert field.validation.max_length == 50
        assert field.validation.pattern == r"^[a-zA-Z0-9_]+$"
        assert field.help_text == "Choose a unique username"

    def test_choices_field_with_validation(self) -> None:
        """Test ChoicesField with validation and choices."""
        choices = [
            FieldChoices(title="Admin", value="admin"),
            FieldChoices(title="User", value="user"),
            FieldChoices(title="Guest", value="guest"),
        ]

        validation = FieldValidation(required=True)

        field = ChoicesField(
            name="role",
            title="User Role",
            field_type="select",
            choices=choices,
            validation=validation,
            required=True,
        )

        assert field.name == "role"
        assert field.title == "User Role"
        assert field.field_type == "select"
        assert len(field.choices) == 3
        assert field.choices[0].title == "Admin"
        assert field.choices[0].value == "admin"
        assert field.validation is not None
        assert field.validation.required is True
        assert field.required is True

    def test_relationship_field_with_validation(self) -> None:
        """Test RelationshipField with validation."""
        validation = FieldValidation(required=True)

        field = RelationshipField(
            name="category",
            title="Category",
            field_type="relationship",
            model="Category",
            id_field="category_id",
            title_field="name",
            validation=validation,
            required=True,
        )

        assert field.name == "category"
        assert field.title == "Category"
        assert field.field_type == "relationship"
        assert field.model == "Category"
        assert field.id_field == "category_id"
        assert field.title_field == "name"
        assert field.validation is not None
        assert field.validation.required is True
        assert field.required is True

    def test_field_error_integration(self) -> None:
        """Test FieldError integration with field validation."""
        field = FieldView(name="test", title="Test", field_type="text", required=True)

        # Simulate validation error
        error = FieldError(code="required", message="This field is required")

        field.error = error

        assert field.error is not None
        assert field.error.code == "required"
        assert field.error.message == "This field is required"

    def test_complex_form_creation(self) -> None:
        """Test creating a complex form with multiple field types."""
        # User registration form
        username_field = FieldView.text_field(
            name="username",
            title="Username",
            required=True,
            validation=FieldValidation(min_length=3, max_length=30),
            placeholder="Enter username",
        )

        email_field = FieldView.email_field(
            name="email",
            title="Email Address",
            required=True,
            placeholder="user@example.com",
        )

        password_field = FieldView.password_field(
            name="password",
            title="Password",
            required=True,
            validation=FieldValidation(min_length=8),
        )

        age_field = FieldView.number_field(
            name="age",
            title="Age",
            validation=FieldValidation(min_value=13, max_value=120),
        )

        role_choices = [
            FieldChoices(title="User", value="user"),
            FieldChoices(title="Moderator", value="moderator"),
            FieldChoices(title="Administrator", value="admin"),
        ]

        role_field = ChoicesField.select_field(
            name="role",
            title="User Role",
            choices=role_choices,
            required=True,
            default_value="user",
        )

        category_field = RelationshipField.relationship_field(
            name="category", title="Category", model="Category", required=False
        )

        newsletter_field = FieldView.checkbox_field(
            name="newsletter", title="Subscribe to Newsletter", default_value=False
        )

        bio_field = FieldView.textarea_field(
            name="bio", title="Biography", placeholder="Tell us about yourself"
        )

        # Verify all fields
        fields = [
            username_field,
            email_field,
            password_field,
            age_field,
            role_field,
            category_field,
            newsletter_field,
            bio_field,
        ]

        assert len(fields) == 8

        # Check specific field properties
        assert username_field.field_type == "text"
        assert email_field.field_type == "text"
        assert email_field.validation is not None
        assert password_field.field_type == "text"
        assert age_field.field_type == "number"
        assert role_field.field_type == "select"
        assert len(role_field.choices) == 3
        assert category_field.field_type == "relationship"
        assert category_field.model == "Category"
        assert newsletter_field.field_type == "checkbox"
        assert bio_field.field_type == "textarea"

    def test_field_serialization_integration(self) -> None:
        """Test that all field types can be serialized together."""
        validation = FieldValidation(required=True, min_length=3)
        choices = [FieldChoices(title="Option", value="opt")]

        fields = [
            FieldView(
                name="text_field",
                title="Text Field",
                field_type="text",
                validation=validation,
            ),
            ChoicesField(
                name="choice_field",
                title="Choice Field",
                field_type="select",
                choices=choices,
            ),
            RelationshipField(
                name="rel_field",
                title="Relationship Field",
                field_type="relationship",
                model="TestModel",
            ),
        ]

        # Serialize all fields
        serialized = [field.model_dump() for field in fields]

        assert len(serialized) == 3

        # Check that each field has the expected structure
        assert serialized[0]["name"] == "text_field"
        assert serialized[0]["field_type"] == "text"
        assert "validation" in serialized[0]

        assert serialized[1]["name"] == "choice_field"
        assert serialized[1]["field_type"] == "select"
        assert "choices" in serialized[1]

        assert serialized[2]["name"] == "rel_field"
        assert serialized[2]["field_type"] == "relationship"
        assert "model" in serialized[2]

    def test_validation_integration(self) -> None:
        """Test that validation works across all field types."""
        # Test text field validation
        text_field = FieldView.text_field(
            name="text",
            title="Text",
            validation=FieldValidation(min_length=3, max_length=10),
        )

        assert text_field.validate_value("abc") == []  # Valid
        assert len(text_field.validate_value("ab")) > 0  # Too short
        assert len(text_field.validate_value("abcdefghijk")) > 0  # Too long

        # Test number field validation
        number_field = FieldView.number_field(
            name="number",
            title="Number",
            validation=FieldValidation(min_value=1, max_value=100),
        )

        assert number_field.validate_value(50) == []  # Valid
        assert len(number_field.validate_value(0)) > 0  # Too low
        assert len(number_field.validate_value(150)) > 0  # Too high

        # Test required field validation
        required_field = FieldView.text_field(
            name="required", title="Required", required=True
        )

        assert len(required_field.validate_value("")) > 0  # Empty
        assert len(required_field.validate_value(None)) > 0  # None
        assert required_field.validate_value("value") == []  # Valid

    def test_widget_integration(self) -> None:
        """Test widget functionality across different field types."""
        # Test default widget assignment
        text_field = FieldView.text_field(name="text", title="Text")
        assert text_field.widget == "text"

        number_field = FieldView.number_field(name="number", title="Number")
        assert number_field.widget == "number"

        checkbox_field = FieldView.checkbox_field(name="checkbox", title="Checkbox")
        assert checkbox_field.widget == "checkbox"

        # Test custom widget assignment
        custom_text_field = FieldView(
            name="custom_text", title="Custom Text", field_type="text", widget="email"
        )
        assert custom_text_field.widget == "email"

        # Test widget-specific factory methods
        toggle_field = FieldView.toggle_field(name="toggle", title="Toggle")
        assert toggle_field.widget == "toggle"
        assert toggle_field.field_type == "checkbox"

        switch_field = FieldView.switch_field(name="switch", title="Switch")
        assert switch_field.widget == "switch"
        assert switch_field.field_type == "checkbox"

        range_field = FieldView.range_field(name="range", title="Range")
        assert range_field.widget == "range"
        assert range_field.field_type == "number"

        slider_field = FieldView.slider_field(name="slider", title="Slider")
        assert slider_field.widget == "slider"
        assert slider_field.field_type == "number"

        richtext_field = FieldView.richtext_field(name="richtext", title="Rich Text")
        assert richtext_field.widget == "richtext"
        assert richtext_field.field_type == "textarea"

        markdown_field = FieldView.markdown_field(name="markdown", title="Markdown")
        assert markdown_field.widget == "markdown"
        assert markdown_field.field_type == "textarea"

    def test_multi_choices_integration(self) -> None:
        """Test MultiChoicesField integration with other components."""
        choices = [
            FieldChoices(title="Tag 1", value="tag1"),
            FieldChoices(title="Tag 2", value="tag2"),
            FieldChoices(title="Tag 3", value="tag3"),
        ]

        # Test different widget types
        multi_select = MultiChoicesField.multi_choice_select_field(
            name="multi_select", title="Multi Select", choices=choices
        )
        assert multi_select.widget == "multi-select"
        assert multi_select.field_type == "select"
        assert len(multi_select.choices) == 3
        assert isinstance(multi_select, MultiChoicesField)
        assert isinstance(multi_select.choices, list)

        tags_field = MultiChoicesField.multi_choice_tags_field(
            name="tags", title="Tags", choices=choices, max_selections=5
        )
        assert tags_field.widget == "tags"
        assert tags_field.max_selections == 5
        assert isinstance(tags_field, MultiChoicesField)
        assert isinstance(tags_field.choices, list)

        chips_field = MultiChoicesField.multi_choice_chips_field(
            name="chips",
            title="Chips",
            choices=choices,
            min_selections=1,
            max_selections=3,
            required=True,
        )
        assert chips_field.widget == "chips"
        assert chips_field.min_selections == 1
        assert chips_field.max_selections == 3

        checkbox_group = MultiChoicesField.checkbox_group_field(
            name="checkbox_group",
            title="Checkbox Group",
            choices=choices,
            required=True,
        )
        assert checkbox_group.widget == "checkbox-group"
        assert checkbox_group.required is True

        # Test validation integration
        assert multi_select.validate_value(["tag1", "tag2"]) == []  # Valid
        assert len(multi_select.validate_value(["invalid"])) > 0  # Invalid choice
        assert (
            len(
                tags_field.validate_value(
                    ["tag1", "tag2", "tag3", "tag1", "tag2", "tag3"]
                )
            )
            > 0
        )  # Too many (6 > max_selections=5)
        assert len(chips_field.validate_value([])) > 0  # Too few

    def test_complex_form_with_widgets(self) -> None:
        """Test creating a complex form with various widgets."""
        # Blog post form with different widgets
        title_field = FieldView.text_field(name="title", title="Title", required=True)

        content_field = FieldView.richtext_field(
            name="content", title="Content", required=True
        )

        status_choices = [
            FieldChoices(title="Draft", value="draft"),
            FieldChoices(title="Published", value="published"),
            FieldChoices(title="Archived", value="archived"),
        ]

        status_field = ChoicesField.radio_field(
            name="status", title="Status", choices=status_choices, required=True
        )

        tag_choices = [
            FieldChoices(title="Technology", value="tech"),
            FieldChoices(title="Design", value="design"),
            FieldChoices(title="Business", value="business"),
        ]

        tags_field = MultiChoicesField.multi_choice_tags_field(
            name="tags", title="Tags", choices=tag_choices, max_selections=5
        )

        featured_field = FieldView.toggle_field(
            name="featured", title="Featured Post", default_value=False
        )

        allow_comments_field = FieldView.switch_field(
            name="allow_comments", title="Allow Comments", default_value=True
        )

        # Verify all fields have correct widgets
        assert title_field.widget == "text"
        assert content_field.widget == "richtext"
        assert status_field.widget == "radio"
        assert tags_field.widget == "tags"
        assert featured_field.widget == "toggle"
        assert allow_comments_field.widget == "switch"

        # Verify field types
        assert title_field.field_type == "text"
        assert content_field.field_type == "textarea"
        assert status_field.field_type == "select"
        assert tags_field.field_type == "select"
        assert featured_field.field_type == "checkbox"
        assert allow_comments_field.field_type == "checkbox"
