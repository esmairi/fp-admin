"""
Unit tests for field relationships.

Tests the RelationshipField class.
"""

import pytest
from pydantic import ValidationError

from fp_admin.admin.fields.relationships import RelationshipField

pytestmark = pytest.mark.unit


class TestRelationshipField:
    """Test cases for RelationshipField."""

    def test_relationship_field_creation(self) -> None:
        """Test basic RelationshipField creation."""
        field = RelationshipField(name="category", title="Category", model="Category")

        assert field.name == "category"
        assert field.title == "Category"
        assert field.field_type == "relationship"
        assert field.model == "Category"
        assert field.id_field == "id"
        assert field.title_field == "title"

    def test_relationship_field_required_fields(self) -> None:
        """Test that name, title, and model are required fields."""
        field = RelationshipField(name="user", title="User", model="User")

        assert field.name == "user"
        assert field.title == "User"
        assert field.model == "User"

    def test_relationship_field_missing_name(self) -> None:
        """Test that name field is required."""
        with pytest.raises(ValidationError):
            RelationshipField(title="Category", model="Category")

    def test_relationship_field_missing_model(self) -> None:
        """Test that model field is required."""
        with pytest.raises(ValidationError):
            RelationshipField(name="category", title="Category")

    def test_relationship_field_default_values(self) -> None:
        """Test that id_field and title_field have correct defaults."""
        field = RelationshipField(name="test", title="Test", model="TestModel")

        assert field.id_field == "id"
        assert field.title_field == "title"

    def test_relationship_field_custom_id_field(self) -> None:
        """Test that id_field can be customized."""
        field = RelationshipField(
            name="test", title="Test", model="TestModel", id_field="custom_id"
        )

        assert field.id_field == "custom_id"
        assert field.title_field == "title"

    def test_relationship_field_custom_title_field(self) -> None:
        """Test that title_field can be customized."""
        field = RelationshipField(
            name="test", title="Test", model="TestModel", title_field="name"
        )

        assert field.id_field == "id"
        assert field.title_field == "name"

    def test_relationship_field_custom_both_fields(self) -> None:
        """Test that both id_field and title_field can be customized."""
        field = RelationshipField(
            name="test",
            title="Test",
            model="TestModel",
            id_field="uuid",
            title_field="display_name",
        )

        assert field.id_field == "uuid"
        assert field.title_field == "display_name"

    def test_relationship_field_factory_method(self) -> None:
        """Test the relationship_field factory method."""
        field = RelationshipField.relationship_field(
            name="category", title="Category", model="Category"
        )

        assert field.name == "category"
        assert field.title == "Category"
        assert field.field_type == "relationship"
        assert field.model == "Category"
        assert field.id_field == "id"
        assert field.title_field == "title"

    def test_relationship_field_factory_with_kwargs(self) -> None:
        """Test that factory method accepts additional kwargs."""
        field = RelationshipField.relationship_field(
            name="user",
            title="User",
            model="User",
            required=True,
            help_text="Select a user",
            id_field="user_id",
            title_field="username",
        )

        assert field.required is True
        assert field.help_text == "Select a user"
        assert field.id_field == "user_id"
        assert field.title_field == "username"

    def test_relationship_field_serialization(self) -> None:
        """Test that RelationshipField can be serialized."""
        field = RelationshipField(
            name="category",
            title="Category",
            model="Category",
            required=True,
            id_field="category_id",
            title_field="category_name",
        )

        data = field.model_dump()

        assert data["name"] == "category"
        assert data["title"] == "Category"
        assert data["field_type"] == "relationship"
        assert data["model"] == "Category"
        assert data["required"] is True
        assert data["id_field"] == "category_id"
        assert data["title_field"] == "category_name"

    def test_relationship_field_from_dict(self) -> None:
        """Test that RelationshipField can be created from dict."""
        data = {
            "name": "user",
            "title": "User",
            "field_type": "relationship",
            "model": "User",
            "id_field": "user_id",
            "title_field": "username",
            "required": True,
        }

        field = RelationshipField(**data)

        assert field.name == "user"
        assert field.title == "User"
        assert field.field_type == "relationship"
        assert field.model == "User"
        assert field.id_field == "user_id"
        assert field.title_field == "username"
        assert field.required is True

    def test_relationship_field_empty_strings(self) -> None:
        """Test that empty strings are allowed for model names."""
        field = RelationshipField(name="test", title="Test", model="")

        assert field.model == ""

    def test_relationship_field_unicode_model_name(self) -> None:
        """Test that unicode characters are handled in model names."""
        field = RelationshipField(name="test", title="Test", model="ModèleAvecAccents")

        assert field.model == "ModèleAvecAccents"
