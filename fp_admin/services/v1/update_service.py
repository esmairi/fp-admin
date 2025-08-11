from typing import Any, Dict, List, Type, TypeVar, Union

from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from fp_admin.admin.models.helpers import get_model_relationship_fields
from fp_admin.exceptions import ModelError, NotFoundError
from fp_admin.registry import view_registry
from fp_admin.schemas import UpdateRecordParams

from .base_service import BaseService
from .helpers import lookup_form_id, validate_allowed_fields
from .read_service import ReadService

T = TypeVar("T", bound=SQLModel)


class UpdateService(BaseService[T]):

    def _validate_form_data_with_existing_record(
        self,
        record_data: Dict[str, Any],
        form_id: str,
        params_data: Dict[str, Any],
    ) -> None:
        """Validate form data with existing record data merged."""

        validation_data = {**record_data, **params_data}

        # Validate Fields
        form_view = view_registry.get_form_view(form_id)
        form_view.validate_update_fields(validation_data)

    async def update_record(
        self,
        session: AsyncSession,
        record_id: int,
        params: UpdateRecordParams,
    ) -> Dict[str, Any]:
        """Update an existing record for a model."""
        form_id = params.form_id
        read_service = ReadService(self.model_class, self.model_info.name)
        existing_record: T = await read_service.get_by_id(
            session, record_id
        )  # type: ignore
        if not existing_record:
            raise NotFoundError(
                details={"resource": self.model_info.name, "identifier": record_id}
            )
        if not form_id:
            form_id = lookup_form_id(
                list(params.data.keys()), self.model_info.name, "update"
            )

        # Validate allowed update fields
        validate_allowed_fields(form_id, params.data, "update")

        # Validate form data
        self._validate_form_data_with_existing_record(
            existing_record.model_dump(), form_id, params.data
        )

        self._update_direct_fields(existing_record, params.data)
        await self._update_relashionships_model(session, existing_record, params.data)

        session.add(existing_record)
        await session.commit()

        fields = list(
            set(self.model_info.direct_fields)
            - set(self.model_info.get_view_excluded_field_names())
        )
        rel_fields = get_model_relationship_fields(self.model_class)
        all_fields = fields + rel_fields

        return await read_service.get_record_by_id(
            session, record_id, all_fields
        )  # type: ignore

    def _update_direct_fields(self, record: T, data: Dict[str, Any]) -> None:
        """Update record fields with provided data."""
        target_fields, _ = self.model_info.get_fields_by_names(list(data.keys()))

        for field in target_fields:
            if hasattr(record, field):
                setattr(record, field, data[field])

    async def _update_relashionships_model(
        self, session: AsyncSession, instance: T, data: Dict[str, Any]
    ) -> None:
        _, rel_fields = self.model_info.get_fields_by_names(list(data.keys()))
        target_fields = set(rel_fields).intersection(set(data.keys()))
        if not target_fields:
            return None
        await session.refresh(instance, attribute_names=target_fields)
        for rel_field in target_fields:
            attr: InstrumentedAttribute[SQLModel] = getattr(self.model_class, rel_field)
            target_model_class = attr.property.entity.class_
            field_value = data[rel_field]
            existing_record = await self.get_existing_records_or_raise(
                session, target_model_class, field_value
            )
            if not existing_record:
                raise ModelError(f"Record  {attr} with {field_value} not found")
            if isinstance(field_value, dict):
                setattr(instance, rel_field, existing_record[0])
            elif isinstance(field_value, list):
                setattr(instance, rel_field, existing_record)
            else:
                raise ValueError(f"Field type not supported: {type(field_value)}")

        return None

    async def get_existing_records_or_raise(
        self,
        session: AsyncSession,
        model: Type[SQLModel],
        identifiers: Union[Dict[str, Any], List[Dict[str, Any]]],
    ) -> List[SQLModel]:
        if isinstance(identifiers, dict):
            identifiers = [identifiers]

        if not identifiers:
            return []

        records: List[SQLModel] = []

        for _, cond in enumerate(identifiers):
            stmt = select(model).where(
                *[getattr(model, field) == value for field, value in cond.items()]
            )
            result = await session.exec(stmt)
            record = result.first()
            if not record:
                raise NotFoundError(f"Record with values {cond} not found.")
            records.append(record)

        return records
