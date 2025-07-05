"""
Unit tests for widget functionality.

Tests the widget types, default assignments, and widget-specific features.
"""

import pytest

from fp_admin.admin.fields import (
    DEFAULT_WIDGETS,
    ChoicesField,
    FieldChoices,
    FieldView,
    MultiChoicesField,
    WidgetType,
)
from fp_admin.admin.fields.validation import FieldValidation

pytestmark = pytest.mark.unit


class TestWidgetTypes:
    """Test widget type definitions and functionality."""

    def test_widget_type_imports(self) -> None:
        """Test that widget types can be imported."""
        assert WidgetType is not None
        assert DEFAULT_WIDGETS is not None
        assert isinstance(DEFAULT_WIDGETS, dict)

    def test_default_widgets_mapping(self) -> None:
        """Test that default widgets mapping is correct."""
        expected_mappings = {
            "text": "text",
            "number": "number",
            "date": "date",
            "checkbox": "checkbox",
            "radio": "radio",
            "select": "select",
            "textarea": "textarea",
            "file": "file",
            "relationship": "select",
        }

        for field_type, expected_widget in expected_mappings.items():
            assert DEFAULT_WIDGETS.get(field_type) == expected_widget

    def test_widget_type_validation(self) -> None:
        """Test that widget types are properly validated."""
        # Valid widget types
        valid_widgets = [
            "text",
            "email",
            "password",
            "search",
            "tel",
            "url",
            "number",
            "range",
            "slider",
            "date",
            "datetime-local",
            "time",
            "month",
            "week",
            "select",
            "radio",
            "checkbox-group",
            "autocomplete",
            "multi-select",
            "tags",
            "chips",
            "file",
            "image",
            "document",
            "textarea",
            "richtext",
            "markdown",
            "checkbox",
            "toggle",
            "switch",
        ]

        # Test that we can create fields with these widget types
        for widget in valid_widgets:
            field = FieldView(
                name=f"test_{widget}",
                title=f"Test {widget}",
                field_type="text",
                widget=widget,
            )
            assert field.widget == widget


class TestWidgetFactoryMethods:
    """Test widget-specific factory methods."""

    def test_select_widget_factories(self) -> None:
        """Test select widget factory methods."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        # Test select field
        select_field = ChoicesField.select_field(
            name="select", title="Select", choices=choices
        )
        assert select_field.widget == "select"
        assert select_field.field_type == "select"

        # Test radio field
        radio_field = ChoicesField.radio_field(
            name="radio", title="Radio", choices=choices
        )
        assert radio_field.widget == "radio"
        assert radio_field.field_type == "select"

        # Test autocomplete field
        autocomplete_field = ChoicesField.autocomplete_field(
            name="autocomplete", title="Autocomplete", choices=choices
        )
        assert autocomplete_field.widget == "autocomplete"
        assert autocomplete_field.field_type == "select"

    def test_multi_select_widget_factories(self) -> None:
        """Test multi-select widget factory methods."""
        choices = [
            FieldChoices(title="Tag 1", value="tag1"),
            FieldChoices(title="Tag 2", value="tag2"),
        ]

        # Test multi-select field
        multi_select = MultiChoicesField.multi_choice_select_field(
            name="multi_select", title="Multi Select", choices=choices
        )
        assert multi_select.widget == "multi-select"
        assert multi_select.field_type == "select"
        assert isinstance(multi_select, MultiChoicesField)
        assert isinstance(multi_select.choices, list)

        # Test tags field
        tags_field = MultiChoicesField.multi_choice_tags_field(
            name="tags", title="Tags", choices=choices
        )
        assert tags_field.widget == "tags"
        assert tags_field.field_type == "select"
        assert isinstance(tags_field, MultiChoicesField)
        assert isinstance(tags_field.choices, list)

        # Test chips field
        chips_field = MultiChoicesField.multi_choice_chips_field(
            name="chips", title="Chips", choices=choices
        )
        assert chips_field.widget == "chips"
        assert chips_field.field_type == "select"

        # Test checkbox group field
        checkbox_group = MultiChoicesField.checkbox_group_field(
            name="checkbox_group", title="Checkbox Group", choices=choices
        )
        assert checkbox_group.widget == "checkbox-group"
        assert checkbox_group.field_type == "select"

    def test_boolean_widget_factories(self) -> None:
        """Test boolean widget factory methods."""
        # Test toggle field
        toggle_field = FieldView.toggle_field(name="toggle", title="Toggle")
        assert toggle_field.widget == "toggle"
        assert toggle_field.field_type == "checkbox"

        # Test switch field
        switch_field = FieldView.switch_field(name="switch", title="Switch")
        assert switch_field.widget == "switch"
        assert switch_field.field_type == "checkbox"

        # Test regular checkbox field
        checkbox_field = FieldView.checkbox_field(name="checkbox", title="Checkbox")
        assert checkbox_field.widget == "checkbox"
        assert checkbox_field.field_type == "checkbox"

    def test_number_widget_factories(self) -> None:
        """Test number widget factory methods."""
        # Test range field
        range_field = FieldView.range_field(name="range", title="Range")
        assert range_field.widget == "range"
        assert range_field.field_type == "number"

        # Test slider field
        slider_field = FieldView.slider_field(name="slider", title="Slider")
        assert slider_field.widget == "slider"
        assert slider_field.field_type == "number"

        # Test regular number field
        number_field = FieldView.number_field(name="number", title="Number")
        assert number_field.widget == "number"
        assert number_field.field_type == "number"

    def test_textarea_widget_factories(self) -> None:
        """Test textarea widget factory methods."""
        # Test richtext field
        richtext_field = FieldView.richtext_field(name="richtext", title="Rich Text")
        assert richtext_field.widget == "richtext"
        assert richtext_field.field_type == "textarea"

        # Test markdown field
        markdown_field = FieldView.markdown_field(name="markdown", title="Markdown")
        assert markdown_field.widget == "markdown"
        assert markdown_field.field_type == "textarea"

        # Test regular textarea field
        textarea_field = FieldView.textarea_field(name="textarea", title="Textarea")
        assert textarea_field.widget == "textarea"
        assert textarea_field.field_type == "textarea"


class TestWidgetIntegration:
    """Test widget integration with other field features."""

    def test_widget_with_validation(self) -> None:
        """Test that widgets work with validation."""
        field = FieldView.toggle_field(
            name="toggle", title="Toggle", validation=FieldValidation(required=True)
        )

        assert field.widget == "toggle"
        assert field.validation is not None
        assert field.validation.required is True

    def test_widget_with_options(self) -> None:
        """Test that widgets work with options."""
        choices = [
            FieldChoices(title="Yes", value=True),
            FieldChoices(title="No", value=False),
        ]

        field = ChoicesField.radio_field(
            name="radio", title="Radio", choices=choices, required=True
        )

        assert field.widget == "radio"
        assert len(field.choices) == 2
        assert field.required is True

    def test_widget_with_constraints(self) -> None:
        """Test that widgets work with selection constraints."""
        choices = [
            FieldChoices(title="Tag 1", value="tag1"),
            FieldChoices(title="Tag 2", value="tag2"),
            FieldChoices(title="Tag 3", value="tag3"),
        ]

        field = MultiChoicesField.multi_choice_tags_field(
            name="tags",
            title="Tags",
            choices=choices,
            min_selections=1,
            max_selections=2,
            required=True,
        )

        assert field.widget == "tags"
        assert field.min_selections == 1
        assert field.max_selections == 2

    def test_widget_serialization(self) -> None:
        """Test that widgets are properly serialized."""
        field = FieldView.range_field(
            name="range", title="Range", help_text="Select a range"
        )

        data = field.model_dump()
        assert data["widget"] == "range"
        assert data["field_type"] == "number"
        assert data["help_text"] == "Select a range"

    def test_widget_from_dict(self) -> None:
        """Test that widgets can be created from dict."""
        data = {
            "name": "custom_field",
            "title": "Custom Field",
            "field_type": "text",
            "widget": "search",
            "placeholder": "Search...",
        }

        field = FieldView(**data)
        assert field.widget == "search"
        assert field.field_type == "text"
        assert field.placeholder == "Search..."


class TestWidgetValidation:
    """Test widget-specific validation."""

    def test_multi_choice_widget_validation(self) -> None:
        """Test validation for multi-choice widgets."""
        choices = [
            FieldChoices(title="Tag 1", value="tag1"),
            FieldChoices(title="Tag 2", value="tag2"),
        ]

        field = MultiChoicesField.multi_choice_tags_field(
            name="tags",
            title="Tags",
            choices=choices,
            min_selections=1,
            max_selections=2,
            required=True,
        )

        # Valid selections
        assert field.validate_value(["tag1"]) == []
        assert field.validate_value(["tag1", "tag2"]) == []

        # Invalid selections
        assert len(field.validate_value([])) > 0  # Too few
        assert (
            len(field.validate_value(["tag1", "tag2", "tag1"])) > 0
        )  # Too many (3 > max_selections=2, even with duplicates)
        assert len(field.validate_value(["invalid"])) > 0  # Invalid choice

    def test_widget_default_behavior(self) -> None:
        """Test that widgets have correct default behavior."""
        # Test that fields get default widgets when not specified
        text_field = FieldView(name="text", title="Text", field_type="text")
        assert text_field.widget == "text"

        number_field = FieldView(name="number", title="Number", field_type="number")
        assert number_field.widget == "number"

        checkbox_field = FieldView(
            name="checkbox", title="Checkbox", field_type="checkbox"
        )
        assert checkbox_field.widget == "checkbox"
