"""
Unit tests for field utilities.

Tests for fp_admin.admin.fields.utils module.
"""

from typing import Any, Literal, Optional, cast

import pytest
from sqlmodel import Field, SQLModel

from fp_admin.admin.fields.utils import (
    _create_validation,
    _format_field_title,
    _get_field_type,
    _get_help_text,
    _get_literal_choices,
    _get_placeholder,
    sqlmodel_to_fieldviews,
)

pytestmark = pytest.mark.unit


class TestSQLModelToFieldViews:
    """Test the sqlmodel_to_fieldviews function."""

    def test_basic_model_conversion(self) -> None:
        """Test basic SQLModel to FieldView conversion."""

        class User(SQLModel):
            name: str = Field()
            age: int = Field()
            is_active: bool = Field(default=True)

        fields = sqlmodel_to_fieldviews(User)

        assert len(fields) == 3

        # Check field types
        name_field = next(f for f in fields if f.name == "name")
        assert name_field.field_type == "text"
        assert name_field.title == "Name"
        assert name_field.required is True

        age_field = next(f for f in fields if f.name == "age")
        assert age_field.field_type == "number"
        assert age_field.title == "Age"

        active_field = next(f for f in fields if f.name == "is_active")
        assert active_field.field_type == "checkbox"
        assert active_field.title == "Is Active"
        assert active_field.default_value is True

    def test_primary_key_skipped(self) -> None:
        """Test that primary key fields are skipped."""

        class User(SQLModel):
            id: int = Field(primary_key=True)
            name: str = Field()
            email: str = Field()

        fields = sqlmodel_to_fieldviews(User)

        # Should only have name and email, not id
        field_names = [f.name for f in fields]
        assert "id" in field_names
        assert "name" in field_names
        assert "email" in field_names
        assert field_names == ["id", "name", "email"]

    def test_literal_types_with_choices(self) -> None:
        """Test Literal types are converted to select fields with choices."""

        class User(SQLModel):
            status: Literal["active", "inactive", "pending"] = Field(default="active")
            role: Literal["admin", "user", "moderator"] = Field(default="user")
            name: str = Field()

        fields = sqlmodel_to_fieldviews(User)

        # Check status field
        status_field = next(f for f in fields if f.name == "status")
        assert status_field.field_type == "select"
        assert status_field.options is not None
        assert len(status_field.options) == 3

        status_choices = [opt["value"] for opt in status_field.options]
        assert "active" in status_choices
        assert "inactive" in status_choices
        assert "pending" in status_choices

        # Check role field
        role_field = next(f for f in fields if f.name == "role")
        assert role_field.field_type == "select"
        assert role_field.options is not None
        assert len(role_field.options) == 3

    def test_optional_fields(self) -> None:
        """Test Optional fields are handled correctly."""

        class User(SQLModel):
            name: str = Field()
            email: Optional[str] = Field(default=None)
            age: Optional[int] = Field(default=None)

        fields = sqlmodel_to_fieldviews(User)

        name_field = next(f for f in fields if f.name == "name")
        assert name_field.required is True

        email_field = next(f for f in fields if f.name == "email")
        assert email_field.required is False

        age_field = next(f for f in fields if f.name == "age")
        assert age_field.required is False

    def test_help_text_extraction(self) -> None:
        """Test that help text is extracted from field descriptions."""

        class User(SQLModel):
            name: str = Field(description="User's full name")
            email: str = Field(description="User's email address")
            age: int = Field()

        fields = sqlmodel_to_fieldviews(User)

        name_field = next(f for f in fields if f.name == "name")
        assert name_field.help_text == "User's full name"

        email_field = next(f for f in fields if f.name == "email")
        assert email_field.help_text == "User's email address"

        age_field = next(f for f in fields if f.name == "age")
        assert age_field.help_text is None


class TestGetFieldType:
    """Test the _get_field_type function."""

    def test_basic_types(self) -> None:
        """Test basic type conversion."""
        assert _get_field_type(str) == "text"
        assert _get_field_type(int) == "number"
        assert _get_field_type(float) == "number"
        assert _get_field_type(bool) == "checkbox"
        assert _get_field_type(list) == "select"

    def test_literal_types(self) -> None:
        """Test Literal type conversion."""
        literal_type = Literal["a", "b", "c"]
        # Cast to Any to avoid Union type issues
        assert _get_field_type(cast(Any, literal_type)) == "select"


class TestGetLiteralChoices:
    """Test the _get_literal_choices function."""

    def test_literal_choices_extraction(self) -> None:
        """Test extracting choices from Literal types."""
        literal_type = Literal["active", "inactive", "pending"]
        # Cast to Any to avoid Union type issues
        choices = _get_literal_choices(cast(Any, literal_type))

        assert choices is not None
        assert len(choices) == 3

        expected_choices = [
            {"title": "Active", "value": "active"},
            {"title": "Inactive", "value": "inactive"},
            {"title": "Pending", "value": "pending"},
        ]

        assert choices == expected_choices

    def test_non_literal_type(self) -> None:
        """Test non-Literal type returns None."""
        # Cast to Any to avoid Union type issues
        choices = _get_literal_choices(cast(Any, str))
        assert choices is None


class TestCreateValidation:
    """Test the _create_validation function."""

    def test_length_validation(self) -> None:
        """Test length validation extraction."""
        field_info = type(
            "MockField",
            (),
            {
                "max_length": 100,
                "min_length": 2,
            },
        )()

        validation = _create_validation(field_info)

        assert validation is not None
        assert validation.max_length == 100
        assert validation.min_length == 2

    def test_value_validation(self) -> None:
        """Test value validation extraction."""
        field_info = type(
            "MockField",
            (),
            {
                "gt": 0,
                "lte": 120,
            },
        )()

        validation = _create_validation(field_info)

        assert validation is not None
        assert validation.min_value == 0
        assert validation.max_value == 120

    def test_no_validation(self) -> None:
        """Test field with no validation returns None."""
        field_info = type("MockField", (), {})()

        validation = _create_validation(field_info)

        assert validation is None


class TestFormatFieldTitle:
    """Test the _format_field_title function."""

    def test_basic_formatting(self) -> None:
        """Test basic field name formatting."""
        assert _format_field_title("user_name") == "User Name"
        assert _format_field_title("email_address") == "Email Address"
        assert _format_field_title("is_active") == "Is Active"

    def test_abbreviation_handling(self) -> None:
        """Test abbreviation handling."""
        assert _format_field_title("user_id") == "User ID"
        assert _format_field_title("api_url") == "API URL"
        assert _format_field_title("api_key") == "API Key"

    def test_single_word(self) -> None:
        """Test single word formatting."""
        assert _format_field_title("name") == "Name"
        assert _format_field_title("email") == "Email"


class TestGetHelpText:
    """Test the _get_help_text function."""

    def test_with_description(self) -> None:
        """Test help text extraction with description."""
        field_info = type(
            "MockField",
            (),
            {
                "description": "User's full name",
            },
        )()

        help_text = _get_help_text(field_info)
        assert help_text == "User's full name"

    def test_without_description(self) -> None:
        """Test help text extraction without description."""
        field_info = type("MockField", (), {})()

        help_text = _get_help_text(field_info)
        assert help_text is None


class TestGetPlaceholder:
    """Test the _get_placeholder function."""

    def test_with_placeholder(self) -> None:
        """Test placeholder extraction with placeholder."""
        field_info = type(
            "MockField",
            (),
            {
                "placeholder": "Enter your name",
            },
        )()

        placeholder = _get_placeholder(field_info)
        assert placeholder == "Enter your name"

    def test_generated_placeholder(self) -> None:
        """Test generated placeholder."""
        field_info = type(
            "MockField",
            (),
            {
                "name": "user_name",
            },
        )()

        placeholder = _get_placeholder(field_info)
        assert placeholder == "Enter user name"

    def test_without_placeholder(self) -> None:
        """Test placeholder extraction without placeholder."""
        field_info = type("MockField", (), {})()

        placeholder = _get_placeholder(field_info)
        assert placeholder is None


class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_complete_model_conversion(self) -> None:
        """Test complete model conversion with all features."""

        class CompleteUser(SQLModel):
            id: int = Field(primary_key=True)
            name: str = Field(description="User's full name")
            email: str = Field(description="User's email")
            age: int = Field(description="User's age")
            status: Literal["active", "inactive"] = Field(default="active")
            is_active: bool = Field(default=True)
            bio: Optional[str] = Field(default=None, description="User's biography")

        fields = sqlmodel_to_fieldviews(CompleteUser)

        # Should have 6 fields (excluding id)
        assert len(fields) == 7

        # Check each field
        field_dict = {f.name: f for f in fields}

        # Name field
        assert field_dict["name"].field_type == "text"
        assert field_dict["name"].help_text == "User's full name"

        # Email field
        assert field_dict["email"].field_type == "text"
        assert field_dict["email"].help_text == "User's email"

        # Age field
        assert field_dict["age"].field_type == "number"
        assert field_dict["age"].help_text == "User's age"

        # Status field
        assert field_dict["status"].field_type == "select"
        assert field_dict["status"].options is not None
        assert len(field_dict["status"].options) == 2

        # Is active field
        assert field_dict["is_active"].field_type == "checkbox"
        assert field_dict["is_active"].default_value is True

        # Bio field
        assert field_dict["bio"].field_type == "text"
        assert field_dict["bio"].required is False
        assert field_dict["bio"].help_text == "User's biography"
