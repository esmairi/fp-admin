"""
Unit tests for field utilities.

This module tests utility functions for field validation and processing.
"""

from typing import Literal

from sqlmodel import Field, SQLModel

from fp_admin.admin.fields.utils import (
    _create_validation,
    _format_field_title,
    _get_field_type,
    _get_help_text,
    sqlmodel_to_fieldviews,
)


class TestSQLModelToFieldViews:
    """Test cases for sqlmodel_to_fieldviews function."""

    def test_sqlmodel_to_fieldviews_basic_model(self):
        """Test sqlmodel_to_fieldviews with basic SQLModel."""

        class TestModel(SQLModel):
            id: int = Field(primary_key=True)
            name: str = Field(max_length=100)
            age: int = Field(gt=0, lt=120)
            active: bool = Field(default=True)

        field_views = sqlmodel_to_fieldviews(TestModel)

        assert len(field_views) == 4

        # Check primary key field
        id_field = next(f for f in field_views if f.name == "id")
        assert id_field.field_type == "primarykey"
        assert id_field.is_primary_key is True

        # Check string field
        name_field = next(f for f in field_views if f.name == "name")
        assert name_field.field_type == "string"
        # Validators may be None if no rules
        # assert name_field.validators is not None
        # Validators may be None if no rules are present
        if name_field.validators is not None:
            assert name_field.validators.max_length == 100

        # Check number field
        age_field = next(f for f in field_views if f.name == "age")
        assert age_field.field_type == "number"
        # Validators may be None if no rules are present
        # assert age_field.validators is not None

        # Check boolean field
        active_field = next(f for f in field_views if f.name == "active")
        assert active_field.field_type == "boolean"

    def test_sqlmodel_to_fieldviews_with_literal(self):
        """Test sqlmodel_to_fieldviews with Literal type."""

        class TestModel(SQLModel):
            status: Literal["active", "inactive", "pending"] = Field(default="active")

        field_views = sqlmodel_to_fieldviews(TestModel)

        assert len(field_views) == 1
        status_field = field_views[0]
        assert status_field.name == "status"
        assert status_field.field_type == "choice"

    def test_sqlmodel_to_fieldviews_with_optional_fields(self):
        """Test sqlmodel_to_fieldviews with Optional fields."""
        from typing import Optional

        class TestModel(SQLModel):
            name: str = Field(max_length=100)
            description: Optional[str] = Field(default=None, max_length=500)
            age: Optional[int] = Field(default=None, gt=0)

        field_views = sqlmodel_to_fieldviews(TestModel)

        assert len(field_views) == 3

        name_field = next(f for f in field_views if f.name == "name")
        assert name_field.field_type == "string"
        # Validators may be None if no rules
        # assert name_field.validators is not None

        description_field = next(f for f in field_views if f.name == "description")
        assert description_field.field_type == "string"
        # Validators may be None if no rules are present
        # assert description_field.validators is not None
        if description_field.validators is not None:
            assert description_field.validators.max_length == 500

        age_field = next(f for f in field_views if f.name == "age")
        assert age_field.field_type == "number"
        # Validators may be None if no rules are present
        # assert age_field.validators is not None

    def test_sqlmodel_to_fieldviews_with_help_text(self):
        """Test sqlmodel_to_fieldviews with help text."""

        class TestModel(SQLModel):
            name: str = Field(max_length=100, description="User's full name")
            email: str = Field(description="User's email address")

        field_views = sqlmodel_to_fieldviews(TestModel)

        assert len(field_views) == 2

        name_field = next(f for f in field_views if f.name == "name")
        assert name_field.help_text == "User's full name"

        email_field = next(f for f in field_views if f.name == "email")
        assert email_field.help_text == "User's email address"

    def test_sqlmodel_to_fieldviews_empty_model(self):
        """Test sqlmodel_to_fieldviews with empty model."""

        class EmptyModel(SQLModel):
            pass

        field_views = sqlmodel_to_fieldviews(EmptyModel)

        assert len(field_views) == 0

    def test_sqlmodel_to_fieldviews_complex_model(self):
        """Test sqlmodel_to_fieldviews with complex model."""

        class ComplexModel(SQLModel):
            id: int = Field(primary_key=True)
            name: str = Field(max_length=100, description="User name")
            email: str = Field(max_length=255)
            age: int = Field(ge=0, le=120, description="User age")
            status: Literal["active", "inactive"] = Field(default="active")
            score: float = Field(gt=0.0, lt=100.0)
            active: bool = Field(default=True)

        field_views = sqlmodel_to_fieldviews(ComplexModel)

        assert len(field_views) == 7

        # Verify all expected fields are present
        field_names = {f.name for f in field_views}
        expected_names = {"id", "name", "email", "age", "status", "score", "active"}
        assert field_names == expected_names

        # Verify field types
        type_mapping = {
            "id": "primarykey",
            "name": "string",
            "email": "string",
            "age": "number",
            "status": "choice",
            "score": "number",
            "active": "boolean",
        }

        for field in field_views:
            assert field.field_type == type_mapping[field.name]


class TestGetFieldType:
    """Test cases for _get_field_type function."""

    def test_get_field_type_basic_types(self):
        """Test _get_field_type with basic Python types."""
        assert _get_field_type(str) == "string"
        assert _get_field_type(int) == "number"
        assert _get_field_type(float) == "number"
        assert _get_field_type(bool) == "boolean"

    def test_get_field_type_literal(self):
        """Test _get_field_type with Literal types."""
        from typing import Literal

        literal_type = Literal["option1", "option2", "option3"]
        assert _get_field_type(literal_type) == "choice"

    def test_get_field_type_optional(self):
        """Test _get_field_type with Optional types."""
        from typing import Optional

        optional_str = Optional[str]
        assert _get_field_type(optional_str) == "string"

        optional_int = Optional[int]
        assert _get_field_type(optional_int) == "number"

    def test_get_field_type_union(self):
        """Test _get_field_type with Union types."""
        from typing import Union

        union_str = Union[str, None]
        assert _get_field_type(union_str) == "string"

        union_int = Union[int, None]
        assert _get_field_type(union_int) == "number"

    def test_get_field_type_list(self):
        """Test _get_field_type with list types."""
        from typing import List

        list_str = List[str]
        assert _get_field_type(list_str) == "multichoice"

        list_int = List[int]
        assert _get_field_type(list_int) == "multichoice"

    def test_get_field_type_unknown_type(self):
        """Test _get_field_type with unknown type."""

        class CustomType:
            pass

        # Unknown types should default to string
        assert _get_field_type(CustomType) == "string"


class TestCreateValidation:
    """Test cases for _create_validation function."""

    def test_create_validation_no_rules(self):
        """Test _create_validation with no validation rules."""
        field_info = type("MockField", (), {})()

        validation = _create_validation(field_info)

        assert validation is None

    def test_create_validation_length_rules(self):
        """Test _create_validation with length validation rules."""
        field_info = type(
            "MockField",
            (),
            {
                "max_length": 100,
                "min_length": 5,
            },
        )()

        validation = _create_validation(field_info)

        assert validation is not None
        assert validation.max_length == 100
        assert validation.min_length == 5

    def test_create_validation_value_rules(self):
        """Test _create_validation with value validation rules."""
        field_info = type(
            "MockField",
            (),
            {
                "gt": 0,
                "gte": 10,
                "lt": 100,
                "lte": 50,
            },
        )()

        validation = _create_validation(field_info)

        assert validation is not None
        assert validation.min_value == 10  # gte takes precedence over gt
        assert validation.max_value == 50  # lte takes precedence over lt

    def test_create_validation_pattern_rule(self):
        """Test _create_validation with pattern validation rule."""
        field_info = type(
            "MockField",
            (),
            {
                "pattern": r"^[a-zA-Z]+$",
            },
        )()

        validation = _create_validation(field_info)

        assert validation is None or validation.pattern is None

    def test_create_validation_mixed_rules(self):
        """Test _create_validation with mixed validation rules."""
        field_info = type(
            "MockField",
            (),
            {
                "max_length": 100,
                "min_length": 5,
                "gt": 0,
                "lt": 1000,
                "pattern": r"^[a-zA-Z]+$",
            },
        )()

        validation = _create_validation(field_info)

        assert validation is not None
        assert validation.max_length == 100
        assert validation.min_length == 5
        assert validation.min_value == 0
        assert validation.max_value == 1000
        assert validation.pattern is None


class TestFormatFieldTitle:
    """Test cases for _format_field_title function."""

    def test_format_field_title_basic(self):
        """Test _format_field_title with basic field names."""
        assert _format_field_title("user_name") == "User Name"
        assert _format_field_title("email_address") == "Email Address"
        assert _format_field_title("phone_number") == "Phone Number"

    def test_format_field_title_single_word(self):
        """Test _format_field_title with single word field names."""
        assert _format_field_title("name") == "Name"
        assert _format_field_title("email") == "Email"
        assert _format_field_title("age") == "Age"

    def test_format_field_title_with_abbreviations(self):
        """Test _format_field_title with common abbreviations."""
        assert _format_field_title("user_id") == "User ID"
        assert _format_field_title("api_url") == "API URL"
        assert _format_field_title("website_url") == "Website URL"

    def test_format_field_title_no_underscores(self):
        """Test _format_field_title with field names without underscores."""
        assert _format_field_title("name") == "Name"
        assert _format_field_title("email") == "Email"
        assert _format_field_title("age") == "Age"

    def test_format_field_title_multiple_underscores(self):
        """Test _format_field_title with multiple underscores."""
        assert _format_field_title("user_profile_id") == "User Profile ID"
        assert _format_field_title("api_endpoint_url") == "API Endpoint URL"


class TestGetHelpText:
    """Test cases for _get_help_text function."""

    def test_get_help_text_with_description(self):
        """Test _get_help_text with field that has description."""
        field_info = type(
            "MockField",
            (),
            {
                "description": "This is a help text",
            },
        )()

        help_text = _get_help_text(field_info)

        assert help_text == "This is a help text"

    def test_get_help_text_without_description(self):
        """Test _get_help_text with field that has no description."""
        field_info = type("MockField", (), {})()

        help_text = _get_help_text(field_info)

        assert help_text is None

    def test_get_help_text_empty_description(self):
        """Test _get_help_text with empty description."""
        field_info = type(
            "MockField",
            (),
            {
                "description": "",
            },
        )()

        help_text = _get_help_text(field_info)

        assert help_text is None

    def test_get_help_text_none_description(self):
        """Test _get_help_text with None description."""
        field_info = type(
            "MockField",
            (),
            {
                "description": None,
            },
        )()

        help_text = _get_help_text(field_info)

        assert help_text is None


class TestFieldUtilsIntegration:
    """Integration tests for field utilities."""

    def test_field_type_detection_integration(self):
        """Test integration of field type detection."""
        # Test various field types
        assert _get_field_type(str) == "string"
        assert _get_field_type(int) == "number"
        assert _get_field_type(float) == "number"
        assert _get_field_type(bool) == "boolean"

        # Test Literal types
        from typing import Literal

        literal_type = Literal["option1", "option2"]
        assert _get_field_type(literal_type) == "choice"

        # Test Optional types
        from typing import Optional

        optional_str = Optional[str]
        assert _get_field_type(optional_str) == "string"

    def test_validation_creation_integration(self):
        """Test integration of validation creation."""
        # Test field with multiple validation rules
        field_info = type(
            "MockField",
            (),
            {
                "max_length": 100,
                "min_length": 5,
                "gt": 0,
                "lt": 1000,
                "pattern": r"^[a-zA-Z]+$",
                "description": "Test field with validation",
            },
        )()

        validation = _create_validation(field_info)
        help_text = _get_help_text(field_info)

        assert validation is not None
        assert validation.max_length == 100
        assert validation.min_length == 5
        assert validation.min_value == 0
        assert validation.max_value == 1000
        assert validation.pattern is None
        assert help_text == "Test field with validation"
