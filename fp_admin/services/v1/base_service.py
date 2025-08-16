import logging
from collections import defaultdict
from typing import Any, Dict, Generic, List, Sequence, Tuple, Type, TypeVar

from sqlalchemy import and_, or_
from sqlalchemy import select as sqlalchemy_select
from sqlalchemy.orm import aliased
from sqlalchemy.sql.functions import func
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from fp_admin.admin.models import get_pk_names
from fp_admin.exceptions import ModelError, ServiceError
from fp_admin.registry import model_registry
from fp_admin.registry.admin_model_config import AdminModelConfig

T = TypeVar("T", bound=SQLModel)

EXCLUDED_FIELD_TYPES = ["password"]
RELATIVE_FIELD_TYPES = ["foreignkey", "many_to_many", "OneToOneField"]


class BaseService(Generic[T]):

    def __init__(self, model_class: Type[T], model_name: str) -> None:
        self.model_class = model_class
        model_info = model_registry.get(model_name)
        if not model_info:
            raise ModelError(f"Model {model_name} not found")
        self.model_info: AdminModelConfig = model_info

    def get_display_fields(self, model: Type[T]) -> str | None:
        try:
            return model_registry.get_by_model_class(model).display_field
        except ModelError:
            return None

    async def reload_relationship_fields(
        self,
        session: AsyncSession,
        record_ids: List[Dict[str, Any]],
        relationship_field: str,
        limit_per_parent: int = 10,
    ) -> Dict[Tuple[Any, ...], List[Dict[str, Any]]] | None:
        """Reloads related field for a list of records, limited per parent."""
        if not record_ids:
            return None

        pk_fields = get_pk_names(self.model_class)
        if not pk_fields:
            return None

        rel_attr = getattr(self.model_class, relationship_field)
        rel_model = rel_attr.property.entity.class_
        display_field = self.get_display_fields(rel_model)
        selected_fields = self._get_selected_fields(rel_model, display_field)

        stmt = self._build_relationship_query(
            parent_model=self.model_class,
            rel_model=rel_model,
            relationship_field=relationship_field,
            selected_fields=selected_fields,
            parent_ids=record_ids,
            pk_fields=pk_fields,
            limit_per_parent=limit_per_parent,
        )

        result = await session.exec(stmt)
        rows = result.all()
        return self._map_rows_by_parent_key(rows, pk_fields, selected_fields)

    def _get_selected_fields(
        self, rel_model: type[SQLModel], display_field: str | None
    ) -> List[str]:
        pk_fields = get_pk_names(rel_model)
        if display_field:
            return list(set(pk_fields + [display_field]))
        return pk_fields

    def _build_relationship_query(  # pylint: disable=R0913,R0917
        self,
        parent_model: type[SQLModel],
        rel_model: type[SQLModel],
        relationship_field: str,
        selected_fields: List[str],
        parent_ids: List[Dict[str, Any]],
        pk_fields: List[str],
        limit_per_parent: int,
    ) -> Any:
        rel_alias = aliased(rel_model)
        parent_pks = [getattr(parent_model, pk) for pk in pk_fields]
        rel_columns = [getattr(rel_alias, f) for f in selected_fields]

        row_number_col = (
            func.row_number()
            .over(
                partition_by=parent_pks,
                order_by=selected_fields[0],
            )
            .label("row_num")
        )

        subquery = (
            sqlalchemy_select(
                *parent_pks,
                *rel_columns,
                row_number_col,
            )
            .join(rel_alias, getattr(parent_model, relationship_field))
            .where(
                *[
                    getattr(parent_model, pk).in_([r[pk] for r in parent_ids])
                    for pk in pk_fields
                ]
            )
            .subquery()
        )

        return sqlalchemy_select(*subquery.c).where(
            subquery.c.row_num <= limit_per_parent
        )

    def _map_rows_by_parent_key(
        self,
        rows: Sequence[Any],
        pk_fields: List[str],
        selected_fields: List[str],
    ) -> Dict[Tuple[Any, ...], List[Dict[str, Any]]]:
        related_map: Dict[Tuple[Any, ...], List[Dict[str, Any]]] = defaultdict(list)
        pk_len = len(pk_fields)

        for row in rows:
            key = tuple(row[:pk_len])
            data = dict(zip(selected_fields, row[pk_len:-1]))  # Exclude row_num
            related_map[key].append(data)

        return related_map

    async def load_records(
        self,
        session: AsyncSession,
        records: List[Dict[str, Any]],
        model: Type[SQLModel],
    ) -> Sequence[SQLModel]:
        if not records:
            raise ValueError("No valid data provided")
        conditions = []

        for record in records:
            sub_conditions = []
            for field_name, value in record.items():
                if not hasattr(model, field_name):
                    raise ValueError(
                        f"Model '{model.__name__}' has no attribute '{field_name}'"
                    )
                sub_conditions.append(getattr(model, field_name) == value)
            conditions.append(and_(*sub_conditions))

        stmt = select(model).where(or_(*conditions))
        result = await session.exec(stmt)
        return result.all()

    async def delete(self, session: AsyncSession, id_: int) -> None:
        obj = await session.get(self.model_class, id_)
        if obj:
            await session.delete(obj)
            await session.commit()
        raise ValueError("No valid field value provided")

    async def filter(
        self, session: AsyncSession, **filters: Any
    ) -> List[Dict[str, Any]]:
        """Filter model instances by criteria.

        Args:
            model_class: The model class
            **filters: Filter criteria

        Returns:
            List of filtered model instances
        """
        try:
            query = select(self.model_class)
            for field, value in filters.items():
                query = query.where(getattr(self.model_class, field) == value)
            records = await session.exec(query)
            return [record.model_dump() for record in records.all()]
        except Exception as e:
            logging.error("Error filtering %s: %s", self.model_class.__name__, e)
            raise ServiceError(
                f"Failed to filter {self.model_class.__name__}: {e}"
            ) from e
