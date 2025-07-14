"""
Unit tests for widget types and configuration.

This module tests the widget types, WidgetConfig, and widget validation functionality.
"""

from typing import get_args

from fp_admin.admin.fields.types import FieldType
from fp_admin.admin.fields.widgets import (
    DEFAULT_WIDGETS,
    VALID_WIDGET_COMBINATIONS,
    WIDGET_TYPES,
    WidgetConfig,
    WidgetType,
    validate_widget_combination,
)


class TestWidgetType:
    """Test cases for WidgetType definitions."""

    def test_widget_type_values(self):
        """Test that WidgetType contains all expected values."""
        for expected_widget in [
            "text",
            "textarea",
            "password",
            "input",
            "Slider",
            "calendar",
            "Checkbox",
            "switch",
            "select",
            "dropdown",
            "radio",
            "multiSelect",
            "chips",
            "listBox",
            "autoComplete",
            "upload",
            "image",
            "editor",
            "colorPicker",
        ]:
            assert expected_widget in WIDGET_TYPES

    def test_widget_type_string_values(self):
        """Test that all WidgetType values are strings."""
        for widget_type in WIDGET_TYPES:
            assert isinstance(widget_type, str)
            assert len(widget_type) > 0

    def test_widget_type_no_duplicates(self):
        """Test that WidgetType values are unique."""
        widget_types = get_args(WidgetType)
        unique_widgets = set(widget_types)
        assert len(widget_types) == len(unique_widgets)

    def test_widget_type_categorization(self):
        """Test that widgets can be categorized by type."""
        string_widgets = {"text", "textarea", "password"}
        number_widgets = {"input", "Slider"}
        date_widgets = {"calendar"}
        boolean_widgets = {"Checkbox", "switch", "select"}
        choice_widgets = {"dropdown", "radio", "select"}
        multichoice_widgets = {"multiSelect", "chips", "listBox"}
        relationship_widgets = {"dropdown", "autoComplete"}
        file_widgets = {"upload", "image"}
        json_widgets = {"editor"}
        color_widgets = {"colorPicker"}

        # Test that all categories are subsets of WIDGET_TYPES
        assert string_widgets.issubset(WIDGET_TYPES)
        assert number_widgets.issubset(WIDGET_TYPES)
        assert date_widgets.issubset(WIDGET_TYPES)
        assert boolean_widgets.issubset(WIDGET_TYPES)
        assert choice_widgets.issubset(WIDGET_TYPES)
        assert multichoice_widgets.issubset(WIDGET_TYPES)
        assert relationship_widgets.issubset(WIDGET_TYPES)
        assert file_widgets.issubset(WIDGET_TYPES)
        assert json_widgets.issubset(WIDGET_TYPES)
        assert color_widgets.issubset(WIDGET_TYPES)


class TestWidgetConfig:
    """Test cases for WidgetConfig class."""

    def test_widget_config_creation_default(self):
        """Test creating WidgetConfig with default values."""
        config = WidgetConfig()

        assert config.timeOnly is False
        assert config.showTime is False
        assert config.mode == "decimal"
        assert config.preview is False
        assert config.editor_type == "monaco"
        assert config.accept is None
        assert config.min is None
        assert config.max is None
        assert config.step is None

    def test_widget_config_creation_with_values(self):
        """Test creating WidgetConfig with custom values."""
        config = WidgetConfig(
            timeOnly=True,
            showTime=True,
            mode="currency",
            preview=True,
            editor_type="ace",
            accept="image/*",
            min=0.0,
            max=100.0,
            step=1.0,
        )

        assert config.timeOnly is True
        assert config.showTime is True
        assert config.mode == "currency"
        assert config.preview is True
        assert config.editor_type == "ace"
        assert config.accept == "image/*"
        assert config.min == 0.0
        assert config.max == 100.0
        assert config.step == 1.0

    def test_widget_config_serialization(self):
        """Test WidgetConfig serialization to dict."""
        config = WidgetConfig(
            timeOnly=True,
            showTime=True,
            mode="currency",
            preview=True,
            editor_type="ace",
            accept="image/*",
            min=0.0,
            max=100.0,
            step=1.0,
        )

        config_dict = config.model_dump()

        assert config_dict["timeOnly"] is True
        assert config_dict["showTime"] is True
        assert config_dict["mode"] == "currency"
        assert config_dict["preview"] is True
        assert config_dict["editor_type"] == "ace"
        assert config_dict["accept"] == "image/*"
        assert config_dict["min"] == 0.0
        assert config_dict["max"] == 100.0
        assert config_dict["step"] == 1.0

    def test_widget_config_from_dict(self):
        """Test creating WidgetConfig from dictionary."""
        config_data = {
            "timeOnly": True,
            "showTime": True,
            "mode": "currency",
            "preview": True,
            "editor_type": "ace",
            "accept": "image/*",
            "min": 0.0,
            "max": 100.0,
            "step": 1.0,
        }

        config = WidgetConfig(**config_data)

        assert config.timeOnly is True
        assert config.showTime is True
        assert config.mode == "currency"
        assert config.preview is True
        assert config.editor_type == "ace"
        assert config.accept == "image/*"
        assert config.min == 0.0
        assert config.max == 100.0
        assert config.step == 1.0

    def test_widget_config_partial_values(self):
        """Test creating WidgetConfig with partial values."""
        config = WidgetConfig(
            timeOnly=True,
            mode="currency",
            min=0.0,
        )

        assert config.timeOnly is True
        assert config.showTime is False  # Default
        assert config.mode == "currency"
        assert config.preview is False  # Default
        assert config.editor_type == "monaco"  # Default
        assert config.accept is None  # Default
        assert config.min == 0.0
        assert config.max is None  # Default
        assert config.step is None  # Default

    def test_widget_config_validation(self):
        """Test WidgetConfig validation."""
        # Test with valid values
        config = WidgetConfig(
            mode="decimal",
            editor_type="monaco",
            accept="image/*",
        )
        assert config.mode == "decimal"
        assert config.editor_type == "monaco"
        assert config.accept == "image/*"

    def test_widget_config_equality(self):
        """Test WidgetConfig equality."""
        config1 = WidgetConfig(timeOnly=True, mode="currency")
        config2 = WidgetConfig(timeOnly=True, mode="currency")
        config3 = WidgetConfig(timeOnly=False, mode="currency")

        assert config1 == config2
        assert config1 != config3


class TestDefaultWidgets:
    """Test cases for DEFAULT_WIDGETS mapping."""

    def test_default_widgets_contains_all_field_types(self):
        """Test that DEFAULT_WIDGETS contains all field types."""
        field_types = get_args(FieldType)

        for field_type in field_types:
            assert field_type in DEFAULT_WIDGETS

    def test_default_widgets_values_are_valid_widgets(self):
        """Test that DEFAULT_WIDGETS values are valid widget types."""
        for default_widget in DEFAULT_WIDGETS.values():
            assert default_widget in WIDGET_TYPES

    def test_default_widgets_string_values(self):
        """Test that all DEFAULT_WIDGETS values are strings."""
        for field_type, default_widget in DEFAULT_WIDGETS.items():
            assert isinstance(default_widget, str)
            assert len(default_widget) > 0

    def test_default_widgets_specific_mappings(self):
        """Test specific default widget mappings."""
        assert DEFAULT_WIDGETS["string"] == "text"
        assert DEFAULT_WIDGETS["number"] == "input"
        assert DEFAULT_WIDGETS["float"] == "input"
        assert DEFAULT_WIDGETS["time"] == "calendar"
        assert DEFAULT_WIDGETS["datetime"] == "calendar"
        assert DEFAULT_WIDGETS["boolean"] == "Checkbox"
        assert DEFAULT_WIDGETS["choice"] == "dropdown"
        assert DEFAULT_WIDGETS["multichoice"] == "multiSelect"
        assert DEFAULT_WIDGETS["foreignkey"] == "dropdown"
        assert DEFAULT_WIDGETS["many_to_many"] == "autoComplete"
        assert DEFAULT_WIDGETS["OneToOneField"] == "dropdown"
        assert DEFAULT_WIDGETS["date"] == "calendar"
        assert DEFAULT_WIDGETS["file"] == "upload"
        assert DEFAULT_WIDGETS["image"] == "image"
        assert DEFAULT_WIDGETS["json"] == "editor"
        assert DEFAULT_WIDGETS["color"] == "colorPicker"
        assert DEFAULT_WIDGETS["primarykey"] == "text"

    def test_default_widgets_no_duplicates(self):
        """Test that DEFAULT_WIDGETS keys are unique."""
        keys = list(DEFAULT_WIDGETS.keys())
        unique_keys = set(keys)
        assert len(keys) == len(unique_keys)


class TestValidWidgetCombinations:
    """Test cases for VALID_WIDGET_COMBINATIONS mapping."""

    def test_valid_widget_combinations_contains_all_field_types(self):
        """Test that VALID_WIDGET_COMBINATIONS contains all field types."""
        field_types = get_args(FieldType)

        for field_type in field_types:
            assert field_type in VALID_WIDGET_COMBINATIONS

    def test_valid_widget_combinations_values_are_lists(self):
        """Test that VALID_WIDGET_COMBINATIONS values are lists."""
        for field_type, valid_widgets in VALID_WIDGET_COMBINATIONS.items():
            assert isinstance(valid_widgets, list)

    def test_valid_widget_combinations_values_are_valid_widgets(self):
        """Test that VALID_WIDGET_COMBINATIONS values are valid widget types."""
        for widgets in VALID_WIDGET_COMBINATIONS.values():
            for widget in widgets:
                assert widget in WIDGET_TYPES

    def test_valid_widget_combinations_specific_mappings(self):
        """Test specific valid widget combinations."""
        # String field can use text, textarea, password
        assert "text" in VALID_WIDGET_COMBINATIONS["string"]
        assert "textarea" in VALID_WIDGET_COMBINATIONS["string"]
        assert "password" in VALID_WIDGET_COMBINATIONS["string"]

        # Number field can use input, Slider
        assert "input" in VALID_WIDGET_COMBINATIONS["number"]
        assert "Slider" in VALID_WIDGET_COMBINATIONS["number"]

        # Boolean field can use Checkbox, switch, select
        assert "Checkbox" in VALID_WIDGET_COMBINATIONS["boolean"]
        assert "switch" in VALID_WIDGET_COMBINATIONS["boolean"]
        assert "select" in VALID_WIDGET_COMBINATIONS["boolean"]

    def test_valid_widget_combinations_no_duplicates(self):
        """Test that VALID_WIDGET_COMBINATIONS keys are unique."""
        keys = list(VALID_WIDGET_COMBINATIONS.keys())
        unique_keys = set(keys)
        assert len(keys) == len(unique_keys)

    def test_valid_widget_combinations_no_duplicate_widgets(self):
        """Test that each field type's valid widgets list has no duplicates."""
        for field_type, valid_widgets in VALID_WIDGET_COMBINATIONS.items():
            unique_widgets = set(valid_widgets)
            assert len(valid_widgets) == len(unique_widgets)


class TestValidateWidgetCombination:
    """Test cases for validate_widget_combination function."""

    def test_validate_widget_combination_valid_combinations(self):
        """Test validate_widget_combination with valid combinations."""
        # String field with valid widgets
        assert validate_widget_combination("string", "text") is True
        assert validate_widget_combination("string", "textarea") is True
        assert validate_widget_combination("string", "password") is True

        # Number field with valid widgets
        assert validate_widget_combination("number", "input") is True
        assert validate_widget_combination("number", "Slider") is True

        # Boolean field with valid widgets
        assert validate_widget_combination("boolean", "Checkbox") is True
        assert validate_widget_combination("boolean", "switch") is True
        assert validate_widget_combination("boolean", "select") is True

    def test_validate_widget_combination_invalid_combinations(self):
        """Test validate_widget_combination with invalid combinations."""
        # String field with invalid widgets
        assert validate_widget_combination("string", "Slider") is False
        assert validate_widget_combination("string", "Checkbox") is False

        # Number field with invalid widgets
        assert validate_widget_combination("number", "textarea") is False
        assert validate_widget_combination("number", "password") is False

        # Boolean field with invalid widgets
        assert validate_widget_combination("boolean", "text") is False
        assert validate_widget_combination("boolean", "input") is False

    def test_validate_widget_combination_unknown_field_type(self):
        """Test validate_widget_combination with unknown field type."""
        # Unknown field type should return empty list, so any widget should be invalid
        assert validate_widget_combination("unknown_type", "text") is False
        assert validate_widget_combination("unknown_type", "input") is False

    def test_validate_widget_combination_all_field_types(self):
        """Test validate_widget_combination for all field types."""
        field_types = get_args(FieldType)

        for field_type in field_types:
            # Test with default widget for this field type
            default_widget = DEFAULT_WIDGETS[field_type]
            assert validate_widget_combination(field_type, default_widget) is True

            # Test with invalid widget
            assert validate_widget_combination(field_type, "invalid_widget") is False

    def test_validate_widget_combination_edge_cases(self):
        """Test validate_widget_combination with edge cases."""
        # Empty string field type
        assert validate_widget_combination("", "text") is False

        # Empty string widget
        assert validate_widget_combination("string", "") is False

        # None values (should handle gracefully)
        assert validate_widget_combination(None, "text") is False  # type: ignore
        assert validate_widget_combination("string", None) is False  # type: ignore

    def test_validate_widget_combination_case_sensitivity(self):
        """Test validate_widget_combination case sensitivity."""
        # Widget names are case-sensitive
        assert validate_widget_combination("string", "Text") is False  # Wrong case
        assert validate_widget_combination("string", "TEXT") is False  # Wrong case
        assert validate_widget_combination("string", "text") is True  # Correct case

        # Field type names are case-sensitive
        assert validate_widget_combination("String", "text") is False  # Wrong case
        assert validate_widget_combination("STRING", "text") is False  # Wrong case
        assert validate_widget_combination("string", "text") is True  # Correct case


class TestWidgetIntegration:
    """Integration tests for widget functionality."""

    def test_widget_config_with_field_validation(self):
        """Test WidgetConfig with field validation scenarios."""
        # Test time field configuration
        time_config = WidgetConfig(timeOnly=True, showTime=False)
        assert time_config.timeOnly is True
        assert time_config.showTime is False

        # Test datetime field configuration
        datetime_config = WidgetConfig(showTime=True, timeOnly=False)
        assert datetime_config.showTime is True
        assert datetime_config.timeOnly is False

        # Test number field configuration
        number_config = WidgetConfig(min=0.0, max=100.0, step=1.0)
        assert number_config.min == 0.0
        assert number_config.max == 100.0
        assert number_config.step == 1.0

    def test_widget_validation_with_config(self):
        """Test widget validation with configuration."""
        # Test valid combinations with config
        assert validate_widget_combination("time", "calendar") is True
        assert validate_widget_combination("datetime", "calendar") is True
        assert validate_widget_combination("number", "input") is True
        assert validate_widget_combination("number", "Slider") is True

    def test_default_widgets_consistency(self):
        """Test that default widgets are consistent with valid combinations."""
        for field_type, default_widget in DEFAULT_WIDGETS.items():
            # Default widget should be in valid combinations for that field type
            assert validate_widget_combination(field_type, default_widget) is True

    def test_widget_type_completeness(self):
        """Test that all widget types are used in valid combinations."""
        # All widget types should be used somewhere
        used_widgets = set()
        for widgets in VALID_WIDGET_COMBINATIONS.values():
            used_widgets.update(widgets)
        assert WIDGET_TYPES.issubset(used_widgets)
