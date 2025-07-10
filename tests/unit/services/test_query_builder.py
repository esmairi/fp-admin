"""
Tests for the QueryBuilderService.
"""

from typing import Dict, List

from sqlmodel import Field, Relationship, SQLModel, select

from fp_admin.services.query_builder import QueryBuilderService


class TestModel(SQLModel, table=True):
    """Test model for query builder tests."""

    id: int = Field(primary_key=True)
    name: str = Field()
    description: str = Field()


class SelfReferentialModel(SQLModel, table=True):
    """Test model with self-referential relationship."""

    id: int = Field(primary_key=True)
    name: str = Field()
    parent_id: int = Field(foreign_key="selfreferentialmodel.id", default=None)

    # Self-referential relationship
    parent: "SelfReferentialModel" = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "SelfReferentialModel.id"},
    )
    children: list["SelfReferentialModel"] = Relationship(back_populates="parent")


class TestQueryBuilderService:
    """Test cases for QueryBuilderService."""

    def test_build_query_basic(self):
        """Test basic query building."""
        service = QueryBuilderService()
        query, count_query = service.build_query(TestModel)

        assert query is not None
        assert count_query is not None

    def test_build_query_with_filters(self):
        """Test query building with filters."""
        service = QueryBuilderService()
        filters: Dict[str, str | List[str] | List[int]] = {"name": "test"}
        query, count_query = service.build_query(TestModel, filters=filters)

        assert query is not None
        assert count_query is not None

    def test_build_query_with_fields(self):
        """Test query building with field selection."""
        service = QueryBuilderService()
        fields = ["id", "name"]
        query, count_query = service.build_query(TestModel, fields=fields)

        assert query is not None
        assert count_query is not None

    def test_build_query_with_self_referential_relationship(self):
        """Test that self-referential relationships are handled with selectinload."""
        service = QueryBuilderService()

        # This should not raise an exception and should use selectinload
        query, count_query = service.build_query(SelfReferentialModel)

        assert query is not None
        assert count_query is not None

    def test_add_pagination(self):
        """Test pagination addition."""
        service = QueryBuilderService()
        base_query = select(TestModel)
        paginated_query = service.add_pagination(base_query, page=2, page_size=10)

        assert paginated_query is not None

    def test_validate_fields_valid(self):
        """Test field validation with valid fields."""
        service = QueryBuilderService()
        fields = ["id", "name"]
        valid_fields = service.validate_fields(TestModel, fields)

        assert valid_fields == fields

    def test_validate_fields_invalid(self):
        """Test field validation with invalid fields."""
        service = QueryBuilderService()
        fields = ["id", "name", "invalid_field"]
        valid_fields = service.validate_fields(TestModel, fields)

        assert "id" in valid_fields
        assert "name" in valid_fields
        assert "invalid_field" not in valid_fields
