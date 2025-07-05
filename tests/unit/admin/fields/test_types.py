"""
Unit tests for field types.

Tests the FieldType definition and type validation.
"""

from typing import Literal, get_args

import pytest

from fp_admin.admin.fields.types import FieldType

pytestmark = pytest.mark.unit


class TestFieldType:
    """Test cases for FieldType."""

    def test_field_type_values(self) -> None:
        """Test that FieldType contains the expected values."""
        expected_types = [
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

        actual_types = get_args(FieldType)
        assert set(actual_types) == set(expected_types)
        assert len(actual_types) == len(expected_types)

    def test_field_type_is_literal(self) -> None:
        """Test that FieldType is a Literal type."""

        assert hasattr(FieldType, "__origin__")
        assert FieldType.__origin__ is Literal

    def test_all_field_types_are_strings(self) -> None:
        """Test that all field type values are strings."""
        field_types = get_args(FieldType)
        for field_type in field_types:
            assert isinstance(field_type, str)
            assert len(field_type) > 0

    def test_field_types_are_unique(self) -> None:
        """Test that all field type values are unique."""
        field_types = get_args(FieldType)
        assert len(field_types) == len(set(field_types))

    def test_field_types_are_lowercase(self) -> None:
        """Test that all field type values are lowercase."""
        field_types = get_args(FieldType)
        for field_type in field_types:
            assert field_type == field_type.lower()

    def test_field_types_no_spaces(self) -> None:
        """Test that field type values don't contain spaces."""
        field_types = get_args(FieldType)
        for field_type in field_types:
            assert " " not in field_type
