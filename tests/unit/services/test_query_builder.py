"""
Tests for QueryBuilderService.
"""

from typing import Dict, List, Union, cast

import pytest
from sqlmodel import Field, SQLModel, select

from fp_admin.services.query_builder import QueryBuilderService


class PTestModel(SQLModel, table=True):
    """Test model for query builder tests."""

    id: int = Field(primary_key=True)
    name: str = Field()
    status: str = Field()
    category: str = Field()


@pytest.mark.unit
class TestQueryBuilderService:
    """Test cases for QueryBuilderService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.query_builder = QueryBuilderService()

    def test_build_query_without_filters(self):
        """Test building a query without filters."""
        query, count_query = self.query_builder.build_query(PTestModel)

        # Verify query structure
        assert str(query).startswith(
            "SELECT ptestmodel.id, ptestmodel.name, ptestmodel.status,"
            " ptestmodel.category"
        )
        assert str(count_query).startswith("SELECT count(*) AS count_1")

    def test_build_query_with_filters(self):
        """Test building a query with filters."""
        filters = cast(
            Dict[str, Union[str, List[str], List[int]]],
            {"status": "active", "category": ["cat1", "cat2"]},
        )
        query, count_query = self.query_builder.build_query(PTestModel, filters=filters)

        # Verify filters are applied
        query_str = str(query).lower()
        assert "status = :status_1" in query_str
        assert "category in" in query_str

    def test_build_query_with_fields(self):
        """Test building a query with field selection."""
        fields = ["id", "name"]
        query, count_query = self.query_builder.build_query(PTestModel, fields=fields)

        # Verify only selected fields are in query
        query_str = str(query).lower()
        assert "ptestmodel.id, ptestmodel.name" in query_str
        assert "ptestmodel.status" not in query_str
        assert "ptestmodel.category" not in query_str

    def test_add_pagination(self):
        """Test adding pagination to a query."""
        query = select(PTestModel)
        paginated_query = self.query_builder.add_pagination(query, page=2, page_size=10)

        # Verify pagination is applied
        query_str = str(paginated_query).lower()
        assert "limit :param_1" in query_str
        assert "offset :param_2" in query_str

    def test_validate_fields_valid(self):
        """Test field validation with valid fields."""
        fields = ["id", "name", "status"]
        valid_fields = self.query_builder.validate_fields(PTestModel, fields)

        assert valid_fields == fields

    def test_validate_fields_invalid(self):
        """Test field validation with invalid fields."""
        fields = ["id", "invalid_field", "name"]
        valid_fields = self.query_builder.validate_fields(PTestModel, fields)

        assert valid_fields == ["id", "name"]

    def test_validate_fields_empty(self):
        """Test field validation with empty fields."""
        valid_fields = self.query_builder.validate_fields(PTestModel, None)
        assert valid_fields == []

        valid_fields = self.query_builder.validate_fields(PTestModel, [])
        assert valid_fields == []

    def test_build_query_with_filters_and_fields(self):
        """Test building a query with both filters and field selection."""
        filters = cast(
            Dict[str, Union[str, List[str], List[int]]], {"status": "active"}
        )
        fields = ["id", "name"]

        query, count_query = self.query_builder.build_query(
            PTestModel, filters=filters, fields=fields
        )

        # Verify both filters and field selection are applied
        query_str = str(query).lower()
        assert "ptestmodel.id, ptestmodel.name" in query_str
        assert "status = :status_1" in query_str
