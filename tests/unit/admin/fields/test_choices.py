"""
Unit tests for field choices.

Tests the FieldChoices and ChoicesField classes.
"""

import pytest
from pydantic import ValidationError

from fp_admin.admin.fields.choices import ChoicesField, FieldChoices, MultiChoicesField

pytestmark = pytest.mark.unit


class TestFieldChoices:
    """Test cases for FieldChoices."""

    def test_field_choices_creation(self) -> None:
        """Test basic FieldChoices creation."""
        choice = FieldChoices(title="Option 1", value="opt1")

        assert choice.title == "Option 1"
        assert choice.value == "opt1"

    def test_field_choices_required_fields(self) -> None:
        """Test that title and value are required fields."""
        # Should work with both fields
        choice = FieldChoices(title="Test", value="test_value")
        assert choice.title == "Test"
        assert choice.value == "test_value"

    def test_field_choices_missing_title(self) -> None:
        """Test that title field is required."""
        with pytest.raises(ValidationError):
            FieldChoices(value="opt1")

    def test_field_choices_missing_value(self) -> None:
        """Test that value field is required."""
        with pytest.raises(ValidationError):
            FieldChoices(title="Option 1")

    def test_field_choices_string_value(self) -> None:
        """Test string value type."""
        choice = FieldChoices(title="String Option", value="string_value")
        assert isinstance(choice.value, str)
        assert choice.value == "string_value"

    def test_field_choices_int_value(self) -> None:
        """Test integer value type."""
        choice = FieldChoices(title="Integer Option", value=42)
        assert isinstance(choice.value, int)
        assert choice.value == 42

    def test_field_choices_bool_value(self) -> None:
        """Test boolean value type."""
        choice = FieldChoices(title="Boolean Option", value=True)
        assert isinstance(choice.value, bool)
        assert choice.value is True

    def test_field_choices_empty_strings(self) -> None:
        """Test that empty strings are allowed."""
        choice = FieldChoices(title="", value="")

        assert choice.title == ""
        assert choice.value == ""

    def test_field_choices_unicode(self) -> None:
        """Test that unicode characters are handled correctly."""
        choice = FieldChoices(
            title="Option avec caractères spéciaux: éàçù", value="unicode_value"
        )

        assert choice.title == "Option avec caractères spéciaux: éàçù"
        assert choice.value == "unicode_value"


class TestChoicesField:
    """Test cases for ChoicesField."""

    def test_choices_field_creation(self) -> None:
        """Test basic ChoicesField creation."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        field = ChoicesField(name="test_field", title="Test Field", choices=choices)

        assert field.name == "test_field"
        assert field.title == "Test Field"
        assert field.field_type == "select"
        assert len(field.choices) == 2
        assert field.choices[0].title == "Option 1"
        assert field.choices[1].title == "Option 2"

    def test_choices_field_default_choices(self) -> None:
        """Test that choices field has empty list by default."""
        field = ChoicesField(name="test", title="Test")

        assert field.choices == []
        assert isinstance(field.choices, list)

    def test_choices_field_factory_methods(self) -> None:
        """Test factory methods for creating choice fields."""
        choices = [
            FieldChoices(title="Yes", value=True),
            FieldChoices(title="No", value=False),
        ]

        # Test select_field factory
        select_field = ChoicesField.select_field(
            name="yes_no", title="Yes/No", choices=choices
        )

        assert select_field.name == "yes_no"
        assert select_field.title == "Yes/No"
        assert select_field.field_type == "select"
        assert len(select_field.choices) == 2

        # Test radio_field factory
        radio_field = ChoicesField.radio_field(
            name="yes_no_radio", title="Yes/No Radio", choices=choices
        )

        assert radio_field.name == "yes_no_radio"
        assert radio_field.title == "Yes/No Radio"
        assert radio_field.field_type == "select"
        assert radio_field.widget == "radio"
        assert len(radio_field.choices) == 2

    def test_choices_field_with_kwargs(self) -> None:
        """Test that factory methods accept additional kwargs."""
        choices = [FieldChoices(title="Option", value="opt")]

        field = ChoicesField.select_field(
            name="test",
            title="Test",
            choices=choices,
            required=True,
            help_text="Choose an option",
        )

        assert field.required is True
        assert field.help_text == "Choose an option"

    def test_choices_field_serialization(self) -> None:
        """Test that ChoicesField can be serialized."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        field = ChoicesField(
            name="test_field", title="Test Field", choices=choices, required=True
        )

        data = field.model_dump()

        assert data["name"] == "test_field"
        assert data["title"] == "Test Field"
        assert data["field_type"] == "select"
        assert data["required"] is True
        assert len(data["choices"]) == 2
        assert data["choices"][0]["title"] == "Option 1"
        assert data["choices"][1]["title"] == "Option 2"

    def test_choices_field_from_dict(self) -> None:
        """Test that ChoicesField can be created from dict."""
        data = {
            "name": "test_field",
            "title": "Test Field",
            "field_type": "select",
            "choices": [
                {"title": "Option 1", "value": "opt1"},
                {"title": "Option 2", "value": "opt2"},
            ],
            "required": True,
        }

        field = ChoicesField(**data)

        assert field.name == "test_field"
        assert field.title == "Test Field"
        assert field.field_type == "select"
        assert field.required is True
        assert len(field.choices) == 2

    def test_choices_field_empty_choices(self) -> None:
        """Test that ChoicesField works with empty choices list."""
        field = ChoicesField(name="empty_field", title="Empty Field", choices=[])

        assert field.choices == []
        assert len(field.choices) == 0


class TestMultiChoicesField:
    """Test cases for MultiChoicesField."""

    def test_multi_choices_field_creation(self) -> None:
        """Test basic MultiChoicesField creation."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        field = MultiChoicesField(
            name="test_field", title="Test Field", choices=choices
        )

        assert field.name == "test_field"
        assert field.title == "Test Field"
        assert field.field_type == "select"
        assert len(field.choices) == 2
        assert field.min_selections is None
        assert field.max_selections is None

    def test_multi_choices_field_defaults(self) -> None:
        """Test that MultiChoicesField has correct defaults."""
        field = MultiChoicesField(name="test", title="Test")

        assert field.choices == []
        assert field.min_selections is None
        assert field.max_selections is None
        assert isinstance(field.choices, list)

    def test_multi_choices_field_factory_methods(self) -> None:
        """Test factory methods for creating multi-choice fields."""
        choices = [
            FieldChoices(title="Tag 1", value="tag1"),
            FieldChoices(title="Tag 2", value="tag2"),
        ]

        # Test multi_select_field factory
        multi_select = MultiChoicesField.multi_choice_select_field(
            name="tags", title="Tags", choices=choices
        )

        assert multi_select.name == "tags"
        assert multi_select.title == "Tags"
        assert multi_select.field_type == "select"
        assert multi_select.widget == "multi-select"
        assert len(multi_select.choices) == 2
        assert isinstance(multi_select, MultiChoicesField)
        assert isinstance(multi_select.choices, list)

        # Test tags_field factory
        tags_field = MultiChoicesField.multi_choice_tags_field(
            name="tags", title="Tags", choices=choices
        )

        assert tags_field.name == "tags"
        assert tags_field.title == "Tags"
        assert tags_field.widget == "tags"
        assert len(tags_field.choices) == 2
        assert isinstance(tags_field, MultiChoicesField)
        assert isinstance(tags_field.choices, list)

        # Test chips_field factory
        chips_field = MultiChoicesField.multi_choice_chips_field(
            name="chips", title="Chips", choices=choices
        )

        assert chips_field.name == "chips"
        assert chips_field.title == "Chips"
        assert chips_field.widget == "chips"
        assert len(chips_field.choices) == 2

        # Test checkbox_group_field factory
        checkbox_group = MultiChoicesField.checkbox_group_field(
            name="checks", title="Checkboxes", choices=choices
        )

        assert checkbox_group.name == "checks"
        assert checkbox_group.title == "Checkboxes"
        assert checkbox_group.widget == "checkbox-group"
        assert len(checkbox_group.choices) == 2

    def test_multi_choices_field_with_constraints(self) -> None:
        """Test MultiChoicesField with min/max selection constraints."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
            FieldChoices(title="Option 3", value="opt3"),
        ]

        field = MultiChoicesField(
            name="constrained_field",
            title="Constrained Field",
            choices=choices,
            min_selections=1,
            max_selections=2,
        )

        assert field.min_selections == 1
        assert field.max_selections == 2
        assert len(field.choices) == 3

    def test_multi_choices_field_validation_empty_required(self) -> None:
        """Test validation for empty required field."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        field = MultiChoicesField(
            name="test", title="Test", choices=choices, required=True
        )

        errors = field.validate_value(None)
        assert "This field is required" in errors

        errors = field.validate_value([])
        assert "This field is required" in errors

    def test_multi_choices_field_validation_empty_optional(self) -> None:
        """Test validation for empty optional field."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        field = MultiChoicesField(
            name="test", title="Test", choices=choices, required=False
        )

        errors = field.validate_value(None)
        assert len(errors) == 0

        errors = field.validate_value([])
        assert len(errors) == 0

    def test_multi_choices_field_validation_not_list(self) -> None:
        """Test validation for non-list value."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        field = MultiChoicesField(name="test", title="Test", choices=choices)

        errors = field.validate_value("not a list")
        assert "Value must be a list of selections" in errors

    def test_multi_choices_field_validation_min_selections(self) -> None:
        """Test validation for minimum selections."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
            FieldChoices(title="Option 3", value="opt3"),
        ]

        field = MultiChoicesField(
            name="test", title="Test", choices=choices, min_selections=2
        )

        errors = field.validate_value(["opt1"])
        assert "Minimum 2 selection(s) required" in errors

        errors = field.validate_value(["opt1", "opt2"])
        assert len(errors) == 0

    def test_multi_choices_field_validation_max_selections(self) -> None:
        """Test validation for maximum selections."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
            FieldChoices(title="Option 3", value="opt3"),
        ]

        field = MultiChoicesField(
            name="test", title="Test", choices=choices, max_selections=2
        )

        errors = field.validate_value(["opt1", "opt2", "opt3"])
        assert "Maximum 2 selection(s) allowed" in errors

        errors = field.validate_value(["opt1", "opt2"])
        assert len(errors) == 0

    def test_multi_choices_field_validation_invalid_choices(self) -> None:
        """Test validation for invalid choice values."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        field = MultiChoicesField(name="test", title="Test", choices=choices)

        errors = field.validate_value(["opt1", "invalid_choice"])
        assert "Invalid selection: invalid_choice" in errors

        errors = field.validate_value(["opt1", "opt2"])
        assert len(errors) == 0

    def test_multi_choices_field_validation_valid_selections(self) -> None:
        """Test validation for valid selections."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
            FieldChoices(title="Option 3", value="opt3"),
        ]

        field = MultiChoicesField(
            name="test",
            title="Test",
            choices=choices,
            min_selections=1,
            max_selections=3,
        )

        errors = field.validate_value(["opt1", "opt3"])
        assert len(errors) == 0

    def test_multi_choices_field_serialization(self) -> None:
        """Test that MultiChoicesField can be serialized."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        field = MultiChoicesField(
            name="test_field",
            title="Test Field",
            choices=choices,
            min_selections=1,
            max_selections=3,
        )

        data = field.model_dump()

        assert data["name"] == "test_field"
        assert data["title"] == "Test Field"
        assert data["field_type"] == "select"
        assert data["min_selections"] == 1
        assert data["max_selections"] == 3
        assert len(data["choices"]) == 2

    def test_multi_choices_field_from_dict(self) -> None:
        """Test that MultiChoicesField can be created from dict."""
        data = {
            "name": "test_field",
            "title": "Test Field",
            "field_type": "select",
            "choices": [
                {"title": "Option 1", "value": "opt1"},
                {"title": "Option 2", "value": "opt2"},
            ],
            "min_selections": 1,
            "max_selections": 2,
        }

        field = MultiChoicesField(**data)

        assert field.name == "test_field"
        assert field.title == "Test Field"
        assert field.field_type == "select"
        assert field.min_selections == 1
        assert field.max_selections == 2
        assert len(field.choices) == 2
