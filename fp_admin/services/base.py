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
from fp_admin.services.utils import get_relationship_fields

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=SQLModel)


@dataclass
class GetAllParams:
    """Parameters for get_all method."""

    page: int = 1
    page_size: int = 20
    filters: Optional[Dict[str, str | List[str] | List[int]]] = None
    fields: Optional[List[str]] = None
    include_relationships: bool = True
    include: Optional[List[str]] = None


class BaseService:
    """Base service class for business logic operations."""

    session: Session

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

    def get_by_id_with_fields(
        self,
        model_class: Type[T],
        item_id: int,
        fields: Optional[List[str]] = None,
        include_relationships: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """Get a model instance by ID and serialize it with field selection.

        Args:
            model_class: The model class
            item_id: The ID of the item
            fields: Optional list of fields to include
            include_relationships: Whether to include relationships

        Returns:
            The serialized record as a dictionary, or None if not found
        """
        try:
            with self.session as session:
                record = session.get(model_class, item_id)
                if not record:
                    return None
                # Serialize the record inside the session context
                if fields:
                    return {field: getattr(record, field, None) for field in fields}
                return self.serialize(record, include_relationships)
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
                model_class,
                filters=params.filters,
                fields=valid_fields,
                include_relationships=params.include_relationships,
            )

            # Add pagination to the main query
            query = self.query_builder.add_pagination(
                query, params.page, params.page_size
            )

            with self.session as session:
                total = session.exec(count_query).one()
                items = session.exec(query).all()

                # Convert items to dictionaries while session is still open
                if valid_fields:
                    items = [
                        (
                            dict(zip(valid_fields, item))
                            if isinstance(item, tuple)
                            else {
                                field: getattr(item, field, None)
                                for field in valid_fields
                            }
                        )
                        for item in items
                    ]
                else:
                    # Use centralized serialization inside session context
                    items = [
                        self.serialize(item, params.include_relationships)
                        for item in items
                    ]

                return items, total
        except Exception as e:
            self.logger.error("Error getting all %s: %s", model_class.__name__, e)
            raise ServiceError(f"Failed to get all {model_class.__name__}: {e}") from e

    def create(
        self,
        model_instance: T,
        include_relationships: bool = True,
    ) -> Dict[str, Any]:
        """Create a new model instance.

        Args:
            model_instance: The model instance to create
            serialize: Whether to serialize the instance before returning
            include_relationships: Whether to include relationships in serialization

        Returns:
            The created model instance or its serialized dict
        """
        try:
            with self.session as session:
                session.add(model_instance)
                session.commit()
                session.refresh(model_instance)
                return self.serialize(model_instance, include_relationships)
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

    def update_with_serialization(
        self,
        model_instance: T,
        include_relationships: bool = True,
    ) -> Dict[str, Any]:
        """Update an existing model instance and serialize it.

        Args:
            model_instance: The model instance to update
            include_relationships: Whether to include relationships in serialization

        Returns:
            The updated model instance as a serialized dictionary
        """
        try:
            with self.session as session:
                session.add(model_instance)
                session.commit()
                session.refresh(model_instance)
                return self.serialize(model_instance, include_relationships)
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

    def filter(self, model_class: Type[T], **filters: Any) -> List[Dict[str, Any]]:
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
                records = session.exec(query).all()
                return [record.model_dump() for record in records]
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

    def serialize_with_relationships(self, item: T) -> Dict[str, Any]:
        """Serialize a model instance including relationships.

        Args:
            item: The model instance to serialize

        Returns:
            Dictionary representation with relationships
        """
        if not hasattr(item, "dict"):
            return dict(item)

        # Get base serialization
        item_dict = item.model_dump(exclude_none=True)

        # Add relationships
        for rel_field in get_relationship_fields(type(item)):
            rel_value = getattr(item, rel_field)
            if rel_value is not None:
                if isinstance(rel_value, list):
                    item_dict[rel_field] = [
                        (
                            rel_item.dict(exclude_none=True)
                            if hasattr(rel_item, "dict")
                            else dict(rel_item)
                        )
                        for rel_item in rel_value
                    ]
                else:
                    item_dict[rel_field] = (
                        rel_value.dict(exclude_none=True)
                        if hasattr(rel_value, "dict")
                        else dict(rel_value)
                    )
        return item_dict

    def serialize(self, item: T, include_relationships: bool = True) -> Dict[str, Any]:
        """Serialize a model instance.

        Args:
            item: The model instance to serialize
            include_relationships: Whether to include relationships

        Returns:
            Dictionary representation of the model instance
        """
        if include_relationships:
            return self.serialize_with_relationships(item)
        return item.model_dump(exclude_none=True)


__all__ = ["BaseService"]
