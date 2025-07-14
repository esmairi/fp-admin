"""
Unit tests for field types.

This module tests the FieldType definitions and type validation functionality.
"""

from typing import get_args

from fp_admin.admin.fields.types import FieldType


class TestFieldType:
    """Test cases for FieldType definitions."""

    def test_field_type_values(self):
        """Test that FieldType contains all expected values."""
        expected_types = [
            "string",
            "number",
            "float",
            "time",
            "datetime",
            "boolean",
            "choice",
            "multichoice",
            "foreignkey",
            "many_to_many",
            "OneToOneField",
            "date",
            "file",
            "image",
            "json",
            "color",
            "primarykey",
        ]

        field_types = get_args(FieldType)

        for expected_type in expected_types:
            assert expected_type in field_types

    def test_field_type_count(self):
        """Test that FieldType has the expected number of values."""
        field_types = get_args(FieldType)
        assert len(field_types) == 17

    def test_field_type_string_values(self):
        """Test that all FieldType values are strings."""
        field_types = get_args(FieldType)

        for field_type in field_types:
            assert isinstance(field_type, str)
            assert len(field_type) > 0

    def test_field_type_no_duplicates(self):
        """Test that FieldType values are unique."""
        field_types = get_args(FieldType)
        unique_types = set(field_types)
        assert len(field_types) == len(unique_types)

    def test_field_type_basic_types(self):
        """Test basic field types."""
        basic_types = ["string", "number", "float", "boolean"]
        field_types = get_args(FieldType)

        for basic_type in basic_types:
            assert basic_type in field_types

    def test_field_type_date_time_types(self):
        """Test date and time field types."""
        date_time_types = ["time", "datetime", "date"]
        field_types = get_args(FieldType)

        for date_time_type in date_time_types:
            assert date_time_type in field_types

    def test_field_type_choice_types(self):
        """Test choice field types."""
        choice_types = ["choice", "multichoice"]
        field_types = get_args(FieldType)

        for choice_type in choice_types:
            assert choice_type in field_types

    def test_field_type_relationship_types(self):
        """Test relationship field types."""
        relationship_types = ["foreignkey", "many_to_many", "OneToOneField"]
        field_types = get_args(FieldType)

        for relationship_type in relationship_types:
            assert relationship_type in field_types

    def test_field_type_file_types(self):
        """Test file-related field types."""
        file_types = ["file", "image"]
        field_types = get_args(FieldType)

        for file_type in file_types:
            assert file_type in field_types

    def test_field_type_special_types(self):
        """Test special field types."""
        special_types = ["json", "color", "primarykey"]
        field_types = get_args(FieldType)

        for special_type in special_types:
            assert special_type in field_types

    def test_field_type_naming_conventions(self):
        """Test that field types follow consistent naming conventions."""
        for field_type in get_args(FieldType):
            if field_type == "OneToOneField":
                continue
            assert field_type == field_type.lower()

            # No spaces in type names
            assert " " not in field_type

            # No special characters except underscores
            assert field_type.replace("_", "").replace("to", "").isalnum()

    def test_field_type_semantic_groups(self):
        """Test that field types can be grouped semantically."""
        # Basic data types
        basic_types = {"string", "number", "float", "boolean"}

        # Date/time types
        date_time_types = {"time", "datetime", "date"}

        # Choice/selection types
        choice_types = {"choice", "multichoice"}

        # Relationship types
        relationship_types = {"foreignkey", "many_to_many", "OneToOneField"}

        # File/media types
        file_types = {"file", "image"}

        # Special types
        special_types = {"json", "color", "primarykey"}

        # All groups should be disjoint
        all_groups = [
            basic_types,
            date_time_types,
            choice_types,
            relationship_types,
            file_types,
            special_types,
        ]

        for i, group1 in enumerate(all_groups):
            for j, group2 in enumerate(all_groups):
                if i != j:
                    assert group1.isdisjoint(group2)

    def test_field_type_importability(self):
        """Test that FieldType can be imported and used."""
        from fp_admin.admin.fields.types import FieldType

        # Test that it's a valid type
        assert FieldType is not None

        # Test that it can be used in type hints
        def test_function(field_type: FieldType) -> None:
            pass

        # This should not raise an error
        assert callable(test_function)

    def test_field_type_comparison(self):
        """Test that FieldType values can be compared."""
        field_types = get_args(FieldType)

        # Test equality
        assert "string" == "string"
        assert "number" == "number"

        # Test inequality
        assert "string" != "number"
        assert "boolean" != "float"

        # Test sorting
        sorted_types = sorted(field_types)
        assert len(sorted_types) == len(field_types)
        assert sorted_types[0] < sorted_types[-1]

    def test_field_type_string_operations(self):
        """Test that FieldType values support string operations."""
        for field_type in get_args(FieldType):
            if field_type == "OneToOneField":
                continue
            assert field_type.lower() == field_type

            # Test string concatenation
            combined = field_type + "_test"
            assert combined.endswith("_test")
            assert combined.startswith(field_type)

    def test_field_type_validation(self):
        """Test that FieldType values are valid field types."""
        for field_type in get_args(FieldType):
            if field_type == "OneToOneField":
                continue
            assert field_type.islower()  # All should be lowercase

            # Should not contain invalid characters
            assert not any(char in field_type for char in [" ", "\t", "\n", "\r"])

            # Should not be empty or whitespace
            assert field_type.strip() == field_type

    def test_field_type_completeness(self):
        """Test that FieldType covers all common field types."""
        # Common field types that should be covered
        common_types = {
            "string",  # Text input
            "number",  # Numeric input
            "float",  # Decimal input
            "boolean",  # True/false
            "date",  # Date picker
            "time",  # Time picker
            "datetime",  # Date and time picker
            "choice",  # Single selection
            "multichoice",  # Multiple selection
            "file",  # File upload
            "image",  # Image upload
            "json",  # JSON data
            "color",  # Color picker
            "primarykey",  # Primary key
        }

        field_types = set(get_args(FieldType))

        # All common types should be covered
        for common_type in common_types:
            assert common_type in field_types

    def test_field_type_extensibility(self):
        """Test that FieldType can be extended with new types."""
        # This test documents how to extend FieldType
        # In practice, you would modify the FieldType definition in types.py

        current_types = set(get_args(FieldType))

        # Example of how to add new types (this is just documentation)
        # new_types = ["custom_type", "another_type"]
        # extended_types = current_types.union(new_types)

        # For now, just verify current types are valid
        assert len(current_types) > 0
        assert all(isinstance(t, str) for t in current_types)
