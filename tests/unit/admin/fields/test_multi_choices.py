"""
Tests for MultiChoicesField functionality.
"""

import pytest

from fp_admin.admin.fields import FieldChoices, MultiChoicesField

pytestmark = pytest.mark.unit


class TestMultiChoicesField:
    """Test MultiChoicesField functionality."""

    def test_multi_select_field_creation(self) -> None:
        """Test creating a multi-select field."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        field = MultiChoicesField.multi_select_field(
            name="test_field", title="Test Field", choices=choices
        )

        assert field.name == "test_field"
        assert field.title == "Test Field"
        assert field.field_type == "select"
        assert field.widget == "multi-select"
        assert len(field.choices) == 2
        assert field.min_selections is None
        assert field.max_selections is None

    def test_tags_field_creation(self) -> None:
        """Test creating a tags field."""
        choices = [
            FieldChoices(title="Tag 1", value="tag1"),
            FieldChoices(title="Tag 2", value="tag2"),
        ]

        field = MultiChoicesField.tags_field(
            name="tags", title="Tags", choices=choices, max_selections=5
        )

        assert field.name == "tags"
        assert field.title == "Tags"
        assert field.widget == "tags"
        assert field.max_selections == 5

    def test_chips_field_creation(self) -> None:
        """Test creating a chips field."""
        choices = [
            FieldChoices(title="Chip 1", value="chip1"),
            FieldChoices(title="Chip 2", value="chip2"),
        ]

        field = MultiChoicesField.chips_field(
            name="chips",
            title="Chips",
            choices=choices,
            min_selections=1,
            max_selections=3,
        )

        assert field.name == "chips"
        assert field.title == "Chips"
        assert field.widget == "chips"
        assert field.min_selections == 1
        assert field.max_selections == 3

    def test_checkbox_group_field_creation(self) -> None:
        """Test creating a checkbox group field."""
        choices = [
            FieldChoices(title="Check 1", value="check1"),
            FieldChoices(title="Check 2", value="check2"),
        ]

        field = MultiChoicesField.checkbox_group_field(
            name="checks", title="Checkboxes", choices=choices, required=True
        )

        assert field.name == "checks"
        assert field.title == "Checkboxes"
        assert field.widget == "checkbox-group"
        assert field.required is True

    def test_validate_value_empty_required(self) -> None:
        """Test validation for empty required field."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        field = MultiChoicesField.multi_select_field(
            name="test", title="Test", choices=choices, required=True
        )

        errors = field.validate_value(None)
        assert "This field is required" in errors

        errors = field.validate_value([])
        assert "This field is required" in errors

    def test_validate_value_empty_optional(self) -> None:
        """Test validation for empty optional field."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        field = MultiChoicesField.multi_select_field(
            name="test", title="Test", choices=choices, required=False
        )

        errors = field.validate_value(None)
        assert len(errors) == 0

        errors = field.validate_value([])
        assert len(errors) == 0

    def test_validate_value_not_list(self) -> None:
        """Test validation for non-list value."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        field = MultiChoicesField.multi_select_field(
            name="test", title="Test", choices=choices
        )

        errors = field.validate_value("not a list")
        assert "Value must be a list of selections" in errors

    def test_validate_value_min_selections(self) -> None:
        """Test validation for minimum selections."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
            FieldChoices(title="Option 3", value="opt3"),
        ]

        field = MultiChoicesField.multi_select_field(
            name="test", title="Test", choices=choices, min_selections=2
        )

        errors = field.validate_value(["opt1"])
        assert "Minimum 2 selection(s) required" in errors

        errors = field.validate_value(["opt1", "opt2"])
        assert len(errors) == 0

    def test_validate_value_max_selections(self) -> None:
        """Test validation for maximum selections."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
            FieldChoices(title="Option 3", value="opt3"),
        ]

        field = MultiChoicesField.multi_select_field(
            name="test", title="Test", choices=choices, max_selections=2
        )

        errors = field.validate_value(["opt1", "opt2", "opt3"])
        assert "Maximum 2 selection(s) allowed" in errors

        errors = field.validate_value(["opt1", "opt2"])
        assert len(errors) == 0

    def test_validate_value_invalid_choices(self) -> None:
        """Test validation for invalid choice values."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
        ]

        field = MultiChoicesField.multi_select_field(
            name="test", title="Test", choices=choices
        )

        errors = field.validate_value(["opt1", "invalid_choice"])
        assert "Invalid selection: invalid_choice" in errors

        errors = field.validate_value(["opt1", "opt2"])
        assert len(errors) == 0

    def test_validate_value_valid_selections(self) -> None:
        """Test validation for valid selections."""
        choices = [
            FieldChoices(title="Option 1", value="opt1"),
            FieldChoices(title="Option 2", value="opt2"),
            FieldChoices(title="Option 3", value="opt3"),
        ]

        field = MultiChoicesField.multi_select_field(
            name="test",
            title="Test",
            choices=choices,
            min_selections=1,
            max_selections=3,
        )

        errors = field.validate_value(["opt1", "opt3"])
        assert len(errors) == 0
