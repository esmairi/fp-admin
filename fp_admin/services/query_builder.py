"""
Query builder service for fp-admin.

This module provides a service for dynamically building database queries
with filtering, field selection, and pagination support.
"""

import logging
from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, select

from fp_admin.exceptions import ServiceError
from fp_admin.services.utils import get_relationship_fields

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=SQLModel)


class QueryBuilderService:
    """Service for building dynamic database queries."""

    def __init__(self) -> None:
        """Initialize the query builder service."""
        self.logger = logging.getLogger(self.__class__.__name__)

    def build_query(
        self,
        model_class: Type[T],
        filters: Optional[Dict[str, str | List[str] | List[int]]] = None,
        fields: Optional[List[str]] = None,
        include_relationships: bool = True,
    ) -> tuple[Any, Any]:
        """Build a query with optional filtering and field selection.

        Args:
            model_class: The model class to query
            filters: Optional dict of field filters where values can be strings or lists
            fields: Optional list of fields to select

        Returns:
            Tuple of (query, count_query)
        """
        try:
            # Build base query
            if fields:
                # Select only specified fields
                select_fields = [getattr(model_class, field) for field in fields]
                query = select(*select_fields)
            else:
                # Select all fields and include relationships
                query = select(model_class)
                # Add relationship loading if enabled
                if include_relationships:
                    query = self._add_relationship_loading(query, model_class)

            # Build count query
            count_query = select(func.count()).select_from(model_class)

            # Apply filters
            if filters:
                query, count_query = self._apply_filters(
                    model_class, query, count_query, filters
                )

            return query, count_query

        except Exception as e:
            self.logger.error(
                "Error building query for %s: %s", model_class.__name__, e
            )
            raise ServiceError(
                f"Failed to build query for {model_class.__name__}: {e}"
            ) from e

    def _add_relationship_loading(self, query: Any, model_class: Type[T]) -> Any:
        """Add relationship loading to the query.

        Args:
            query: The query to add relationship loading to
            model_class: The model class

        Returns:
            Query with relationship loading
        """
        # Get all relationship fields from the model
        relationships = get_relationship_fields(model_class)
        for rel_name in relationships:
            rel = getattr(model_class, rel_name)

            # Check if this is a self-referential relationship
            is_self_referential = (
                hasattr(rel.property, "mapper")
                and rel.property.mapper.class_ == model_class
            )

            if is_self_referential:
                # For self-referential relationships, use selectinload instead of join
                # This avoids the SQLAlchemy join error
                self.logger.debug(
                    "Using selectinload for self-referential relationship '%s' for %s",
                    rel_name,
                    model_class.__name__,
                )
                query = query.options(selectinload(rel))
            else:
                # For regular relationships, use join
                query = query.join(rel, isouter=True)

        return query

    def _apply_filters(
        self,
        model_class: Type[T],
        query: Any,
        count_query: Any,
        filters: Dict[str, str | List[str] | List[int]],
    ) -> tuple[Any, Any]:
        """Apply filters to both the main query and count query.

        Args:
            model_class: The model class
            query: The main query to apply filters to
            count_query: The count query to apply filters to
            filters: Dictionary of field filters

        Returns:
            Tuple of (filtered_query, filtered_count_query)
        """
        for field, value in filters.items():
            if not hasattr(model_class, field):
                self.logger.warning(
                    "Field '%s' not found in model %s", field, model_class.__name__
                )
                continue

            field_attr = getattr(model_class, field)

            if isinstance(value, list):
                # Handle list values (IN clause)
                query = query.where(field_attr.in_(value))
                count_query = count_query.where(field_attr.in_(value))
            else:
                # Handle single values (equality)
                query = query.where(field_attr == value)
                count_query = count_query.where(field_attr == value)

        return query, count_query

    def add_pagination(self, query: Any, page: int = 1, page_size: int = 20) -> Any:
        """Add pagination to a query.

        Args:
            query: The query to paginate
            page: Page number (1-based)
            page_size: Items per page

        Returns:
            Paginated query
        """
        offset = (page - 1) * page_size
        return query.offset(offset).limit(page_size)

    def validate_fields(
        self, model_class: Type[T], fields: Optional[List[str]] = None
    ) -> List[str]:
        """Validate that the requested fields exist in the model.

        Args:
            model_class: The model class
            fields: List of field names to validate

        Returns:
            List of valid field names
        """
        if not fields:
            return []

        valid_fields = []
        model_fields = (
            model_class.model_fields if hasattr(model_class, "model_fields") else {}
        )

        for field in fields:
            if field in model_fields or hasattr(model_class, field):
                valid_fields.append(field)
            else:
                self.logger.warning(
                    "Field '%s' not found in model %s", field, model_class.__name__
                )

        return valid_fields


__all__ = ["QueryBuilderService"]
