"""
Base service class for fp-admin.

This module provides the base service class that all business logic
services should inherit from.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type, TypeVar, cast

from sqlalchemy import func
from sqlmodel import Session, SQLModel, select

from fp_admin.core.database import db_manager
from fp_admin.exceptions import ServiceError
from fp_admin.services.query_builder import QueryBuilderService

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=SQLModel)


@dataclass
class GetAllParams:
    """Parameters for get_all method."""

    page: int = 1
    page_size: int = 20
    filters: Optional[Dict[str, str | List[str] | List[int]]] = None
    fields: Optional[List[str]] = None


class BaseService:
    """Base service class for business logic operations."""

    def __init__(self, session: Session) -> None:
        """Initialize the service."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = session
        self.query_builder = QueryBuilderService()

    def get_by_id(self, model_class: Type[T], item_id: int) -> Optional[T]:
        """Get a model instance by ID.

        Args:
            model_class: The model class
            item_id: The ID of the item

        Returns:
            The model instance or None if not found
        """
        try:
            with self.session as session:
                return cast(Optional[T], session.get(model_class, item_id))
        except Exception as e:
            self.logger.error(
                "Error getting %s by ID %s: %s", model_class.__name__, item_id, e
            )
            raise ServiceError(
                f"Failed to get {model_class.__name__} by ID: {e}"
            ) from e

    def get_all(
        self,
        model_class: Type[T],
        params: GetAllParams,
    ) -> tuple[List[Dict[str, Any]], int]:
        """Get all instances of a model with pagination, filtering, and field selection.

        Args:
            model_class: The model class
            params: Parameters for pagination, filtering, and field selection

        Returns:
            Tuple of (items, total count)
        """
        try:
            # Validate fields
            valid_fields = self.query_builder.validate_fields(
                model_class, params.fields
            )

            # Build queries using QueryBuilderService
            query, count_query = self.query_builder.build_query(
                model_class, filters=params.filters, fields=valid_fields
            )

            # Add pagination to the main query
            query = self.query_builder.add_pagination(
                query, params.page, params.page_size
            )

            with self.session as session:
                total = session.exec(count_query).one()
                items = session.exec(query).all()

            # Convert items to dictionaries
            if valid_fields:
                items = [
                    {field: getattr(item, field, None) for field in valid_fields}
                    for item in items
                ]
            else:
                items = [
                    item.dict() if hasattr(item, "dict") else dict(item)
                    for item in items
                ]

            return items, total
        except Exception as e:
            self.logger.error("Error getting all %s: %s", model_class.__name__, e)
            raise ServiceError(f"Failed to get all {model_class.__name__}: {e}") from e

    def create(self, model_instance: T) -> T:
        """Create a new model instance.

        Args:
            model_instance: The model instance to create

        Returns:
            The created model instance
        """
        try:
            with db_manager.get_session() as session:
                session.add(model_instance)
                session.commit()
                session.refresh(model_instance)
                return model_instance
        except Exception as e:
            self.logger.error(
                "Error creating %s: %s", model_instance.__class__.__name__, e
            )
            raise ServiceError(
                f"Failed to create {model_instance.__class__.__name__}: {e}"
            ) from e

    def update(self, model_instance: T) -> T:
        """Update an existing model instance.

        Args:
            model_instance: The model instance to update

        Returns:
            The updated model instance
        """
        try:
            with db_manager.get_session() as session:
                session.add(model_instance)
                session.commit()
                session.refresh(model_instance)
                return model_instance
        except Exception as e:
            self.logger.error(
                "Error updating %s: %s", model_instance.__class__.__name__, e
            )
            raise ServiceError(
                f"Failed to update {model_instance.__class__.__name__}: {e}"
            ) from e

    def delete(self, model_instance: T) -> bool:
        """Delete a model instance.

        Args:
            model_instance: The model instance to delete

        Returns:
            True if deletion was successful
        """
        try:
            with db_manager.get_session() as session:
                session.delete(model_instance)
                session.commit()
                return True
        except Exception as e:
            self.logger.error(
                "Error deleting %s: %s", model_instance.__class__.__name__, e
            )
            raise ServiceError(
                f"Failed to delete {model_instance.__class__.__name__}: {e}"
            ) from e

    def delete_by_id(self, model_class: Type[T], item_id: int) -> bool:
        """Delete a model instance by ID.

        Args:
            model_class: The model class
            item_id: The ID of the item to delete

        Returns:
            True if deletion was successful
        """
        try:
            with db_manager.get_session() as session:
                instance = session.get(model_class, item_id)
                if instance:
                    session.delete(instance)
                    session.commit()
                    return True
                return False
        except Exception as e:
            self.logger.error(
                "Error deleting %s by ID %s: %s", model_class.__name__, item_id, e
            )
            raise ServiceError(
                f"Failed to delete {model_class.__name__} by ID: {e}"
            ) from e

    def count(self, model_class: Type[T]) -> int:
        """Count the number of instances of a model.

        Args:
            model_class: The model class

        Returns:
            The count of instances
        """
        try:
            with db_manager.get_session() as session:
                stmt = select(func.count()).select_from(model_class)
                return session.exec(stmt).one()
        except Exception as e:
            self.logger.error("Error counting %s: %s", model_class.__name__, e)
            raise ServiceError(f"Failed to count {model_class.__name__}: {e}") from e

    def exists(self, model_class: Type[T], **filters: Any) -> bool:
        """Check if an instance exists with the given filters.

        Args:
            model_class: The model class
            **filters: Filter criteria

        Returns:
            True if an instance exists, False otherwise
        """
        try:
            with db_manager.get_session() as session:
                query = select(model_class)
                for field, value in filters.items():
                    query = query.where(getattr(model_class, field) == value)
                return session.exec(query).first() is not None
        except Exception as e:
            self.logger.error(
                "Error checking existence of %s: %s", model_class.__name__, e
            )
            raise ServiceError(
                f"Failed to check existence of {model_class.__name__}: {e}"
            ) from e

    def filter(self, model_class: Type[T], **filters: Any) -> List[T]:
        """Filter model instances by criteria.

        Args:
            model_class: The model class
            **filters: Filter criteria

        Returns:
            List of filtered model instances
        """
        try:
            with db_manager.get_session() as session:
                query = select(model_class)
                for field, value in filters.items():
                    query = query.where(getattr(model_class, field) == value)
                return cast(List[T], session.exec(query).all())
        except Exception as e:
            self.logger.error("Error filtering %s: %s", model_class.__name__, e)
            raise ServiceError(f"Failed to filter {model_class.__name__}: {e}") from e

    def bulk_create(self, model_instances: List[T]) -> List[T]:
        """Create multiple model instances in bulk.

        Args:
            model_instances: List of model instances to create

        Returns:
            List of created model instances
        """
        try:
            with db_manager.get_session() as session:
                session.add_all(model_instances)
                session.commit()
                for instance in model_instances:
                    session.refresh(instance)
                return model_instances
        except Exception as e:
            self.logger.error(
                "Error bulk creating %s instances: %s", len(model_instances), e
            )
            raise ServiceError(f"Failed to bulk create instances: {e}") from e

    def bulk_update(self, model_instances: List[T]) -> List[T]:
        """Update multiple model instances in bulk.

        Args:
            model_instances: List of model instances to update

        Returns:
            List of updated model instances
        """
        try:
            with db_manager.get_session() as session:
                for instance in model_instances:
                    session.add(instance)
                session.commit()
                for instance in model_instances:
                    session.refresh(instance)
                return model_instances
        except Exception as e:
            self.logger.error(
                "Error bulk updating %s instances: %s", len(model_instances), e
            )
            raise ServiceError(f"Failed to bulk update instances: {e}") from e


__all__ = ["BaseService"]
