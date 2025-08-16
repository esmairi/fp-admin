from typing import Any, Dict, List, Optional, Sequence, Tuple, Type, TypeVar

from sqlalchemy import and_, or_
from sqlalchemy.engine.row import Row
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from fp_admin.admin.models import get_pk_names
from fp_admin.exceptions import ServiceError
from fp_admin.schemas import GetRecordsParams, PaginatedResponse

from .base_service import BaseService
from .query_builder import QueryBuilderService

T = TypeVar("T", bound=SQLModel)


class ListService(BaseService[T]):

    def __init__(self, model: Type[T], model_name: str) -> None:
        super().__init__(model, model_name)
        self.query_builder = QueryBuilderService()

    async def _build_select_statement(
        self,
        model: Type[SQLModel],
        direct_fields: List[str],
        record_ids: List[Dict[str, Any]],
    ) -> Any:
        primary_keys = get_pk_names(model)
        fields = [getattr(model, field) for field in direct_fields]
        stmt = select(*fields)

        if len(primary_keys) == 1:
            pk = primary_keys[0]
            pk_col = getattr(model, pk)
            stmt = stmt.where(pk_col.in_([r[pk] for r in record_ids]))
        else:
            conditions = [
                and_(*(getattr(model, pk) == rec[pk] for pk in primary_keys))
                for rec in record_ids
            ]
            stmt = stmt.where(or_(*conditions))
        return stmt

    def _as_dicts(
        self, records: Sequence[Any], fields: List[str]
    ) -> List[Dict[str, Any]]:
        return [
            dict(zip(fields, record if isinstance(record, Row) else (record,)))
            for record in records
        ]

    def _attach_relationship(
        self,
        records_dict: List[Dict[str, Any]],
        rel_data: Dict[Tuple[Any, ...], Any],
        rel_name: str,
        primary_keys: List[str],
    ) -> None:
        for ids, rel_value in rel_data.items():
            partial = dict(zip(primary_keys, ids))
            for record in records_dict:
                if all(record[pk] == partial[pk] for pk in primary_keys):
                    record[rel_name] = rel_value
                    break

    async def bulk_reload(
        self,
        session: AsyncSession,
        record_ids: List[Dict[str, int | str]],
        direct_fields: List[str],
        relationship_fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Reloads SQLModel instances from DB with optional relationships."""
        primary_keys = get_pk_names(self.model_class)
        stmt = await self._build_select_statement(
            self.model_class, direct_fields, record_ids
        )
        result = await session.exec(stmt)
        records_dict = self._as_dicts(result.all(), direct_fields)

        if not relationship_fields:
            return records_dict

        for rel in relationship_fields:
            rel_records = await self.reload_relationship_fields(
                session, record_ids, rel
            )
            if rel_records:
                self._attach_relationship(records_dict, rel_records, rel, primary_keys)

        return records_dict

    async def list(
        self,
        session: AsyncSession,
        params: GetRecordsParams,
    ) -> PaginatedResponse:
        """Get paginated records for a model."""
        valid_fields = self.query_builder.validate_fields(
            self.model_class, params.fields
        )

        if not valid_fields:
            exclude_fields = self.model_info.get_view_excluded_field_names()
            valid_fields = [
                field_name
                for field_name in self.model_info.direct_fields
                if field_name not in exclude_fields
            ]

        fields, relationship_fields = self.model_info.get_fields_by_names(valid_fields)
        fields = list({*self.model_info.primary_keys, *fields})

        record_ids, total = await self.list_ids(session, params)
        records = await self.bulk_reload(
            session, record_ids, list(fields), list(relationship_fields)
        )
        total_pages = (total + params.page_size - 1) // params.page_size if total else 1

        return PaginatedResponse(
            data=records,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_prev=params.page > 1,
        )

    async def list_ids(
        self,
        session: AsyncSession,
        params: GetRecordsParams,
    ) -> tuple[List[Dict[str, Any]], int]:
        """Get all instances of a model with pagination, filtering, and field selection.

        Args:
            params: Parameters for pagination, filtering, and field selection

        Returns:
            Tuple of (items, total count)
        """
        try:
            primary_keys = get_pk_names(self.model_class)

            # Build queries using QueryBuilderService
            query, count_query = self.query_builder.build_query(
                self.model_class,
                pks=primary_keys,
                filters={},  # add filters
            )

            # Add pagination to the main query
            query = self.query_builder.add_pagination(
                query, params.page, params.page_size
            )

            total_q = await session.exec(count_query)
            items_q = await session.exec(query)
            total = total_q.one()
            items = items_q.all()

            return [
                dict(zip(primary_keys, row if isinstance(row, tuple) else (row,)))
                for row in items
            ], total
        except Exception as e:
            raise ServiceError(
                f"Failed to get all {self.model_class.__name__}: {e}"
            ) from e
