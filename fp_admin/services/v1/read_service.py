from typing import Any, Dict, List, Optional, TypeVar

from sqlalchemy.engine.row import Row
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from fp_admin.admin.models import get_pk_names
from fp_admin.exceptions import NotFoundError

from .base_service import BaseService

T = TypeVar("T", bound=SQLModel)


class ReadService(BaseService[T]):

    async def get_record_by_id(
        self,
        session: AsyncSession,
        record_id: int | str,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, Any] | T:
        """Get a single record by ID."""

        if not fields:
            exclude_fields = self.model_info.get_view_excluded_field_names()
            fields = [
                field_name
                for field_name in self.model_info.direct_fields
                if field_name not in exclude_fields
            ]

        direct_fields, relationship_fields = self.model_info.get_fields_by_names(fields)
        direct_fields = list({*self.model_info.primary_keys, *direct_fields})

        record = await self.get_by_id(
            session, record_id, direct_fields, relationship_fields
        )
        if not record:
            raise NotFoundError(
                details={"resource": self.model_info.name, "identifier": record_id}
            )
        return record

    async def get_by_id(
        self,
        session: AsyncSession,
        id_: int | str,
        field_names: Optional[List[str]] = None,
        relationship_fields: Optional[List[str]] = None,
    ) -> T | Dict[str, Any] | None:
        if field_names:
            pk_names = get_pk_names(self.model_class)
            if not pk_names:
                raise AttributeError(
                    f"'{self.model_class.__name__}' has no primary key"
                )
            if len(pk_names) > 1:
                raise AttributeError(
                    f"'{self.model_class.__name__}' has more than one primary key"
                )

            fields = self.get_selected_fields(field_names)
            if not fields:
                raise ValueError("No valid field value provided")

            stmt = select(*fields).where(getattr(self.model_class, pk_names[0]) == id_)
            result = await session.exec(stmt)
            row = result.first()
            if not row:
                raise NotFoundError(
                    details={"resource": self.model_info.name, "identifier": id_}
                )
            row_dict = dict(zip(field_names, row if isinstance(row, Row) else (row,)))

            if relationship_fields:
                for rl_field in relationship_fields:
                    rel_values = await self.reload_relationship_fields(
                        session, [{pk_names[0]: id_}], relationship_field=rl_field
                    )
                    if rel_values:
                        row_dict[rl_field] = rel_values[(id_,)]  # type: ignore
            return row_dict
        return await session.get(self.model_class, id_)

    def get_selected_fields(
        self, field_names: List[str]
    ) -> List[InstrumentedAttribute[T]]:
        fields = []
        for field in field_names:
            if not hasattr(self.model_class, field):
                raise AttributeError(
                    f"'{self.model_class.__name__}' has no field '{field}'"
                )
            fields.append(getattr(self.model_class, field))
        return fields
