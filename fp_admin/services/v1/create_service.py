from typing import Any, Dict, List, TypeVar

from sqlalchemy.orm.collections import InstrumentedList
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from fp_admin.admin.models import get_pk_names
from fp_admin.models.field import FpField
from fp_admin.registry import model_registry, view_registry
from fp_admin.schemas import CreateRecordParams

from .base_service import BaseService
from .helpers import (
    lookup_form_id,
    validate_allowed_fields,
)

T = TypeVar("T", bound=SQLModel)


class CreateService(BaseService[T]):

    async def db_create(self, session: AsyncSession, obj: T) -> T:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def create_record(
        self,
        session: AsyncSession,
        params: CreateRecordParams,
        serialize_response: bool = True,
    ) -> Dict[str, Any] | T:
        """Create a new record for a model."""
        payload = params.data
        form_id = params.form_id
        if not form_id:
            form_id = lookup_form_id(
                list(payload.keys()), self.model_info.name, "create"
            )

        # Validate allowed creation fields
        validate_allowed_fields(form_id, params.data, "create")

        # Validate form data if form_id is provided
        if not form_id:
            raise ValueError("Form ID is required")

        # Validate Fields
        form_view = view_registry.get_form_view(form_id)
        form_view.validate_create_fields(payload)

        model_instance = await self.build_field_from_dict(session, payload, form_id)
        record = await self.db_create(
            session,
            model_instance,
        )
        if serialize_response:
            return await self.serialize(session, record)
        return record

    async def build_field_from_dict(
        self, session: AsyncSession, data: Dict[str, Any], form_id: str
    ) -> T:
        field_names = list(data.keys())
        relative_fields = self.model_info.get_view_relationship_fields(form_id)
        direct_fields, target_relative_field_names = (
            self.model_info.get_fields_by_names_and_form_id(field_names, form_id)
        )

        if direct_fields:
            instance = self.model_class(**{k: data[k] for k in direct_fields})
        else:
            instance = self.model_class()

        def get_field_by_name(field_name: str) -> FpField:
            target_fields = [
                field_view
                for field_view in relative_fields
                if field_view.name == field_name
            ]
            return target_fields[0]

        for field in target_relative_field_names:
            field_object = get_field_by_name(field)
            field_value = data[field]

            # if not issubclass(type(field_value), list):
            #     field_value = [field_value]

            if issubclass(type(field_value), list) and field_object.field_type in [
                "many_to_many"
            ]:  # many2many
                if field_value:
                    related_fields_value = await self.load_records(
                        session, field_value, field_object.model_class
                    )
                    if not related_fields_value:
                        raise ValueError(
                            f"Failed to load {field}  with value = {field_value} "
                        )
                else:
                    related_fields_value = []
                setattr(instance, field, related_fields_value)

            elif field_value and field_object.field_type in [
                "foreign_key",
                "one_to_one",
            ]:
                if issubclass(type(field_value), dict):
                    related_fields_value = await self.load_records(
                        session, field_value, field_object.model_class
                    )
                    if related_fields_value and len(related_fields_value) == 1:
                        setattr(instance, field, related_fields_value[0])
                    else:
                        raise ValueError(
                            f"Failed to load {field}  with value = {field_value} "
                        )
                else:
                    setattr(instance, field, field_value)

        return instance

    async def serialize(self, session: AsyncSession, obj: T) -> Dict[str, Any]:
        direct_fields = self.model_info.direct_fields
        relationship_fields = self.model_info.relationship_fields
        exclude_fields = self.model_info.get_view_excluded_field_names()

        # Load only requested relationships
        if relationship_fields:
            await session.refresh(obj, attribute_names=relationship_fields)

        # Dump core fields (excluding rels)
        model_dump_kwargs: Dict[str, Any] = {}
        if direct_fields:
            model_dump_kwargs["include"] = set(direct_fields)
        if exclude_fields:
            model_dump_kwargs["exclude"] = set(exclude_fields)

        data = obj.model_dump(**model_dump_kwargs)

        # Add relationship data
        for rel_field in relationship_fields:
            rel_value = getattr(obj, rel_field)
            data[rel_field] = self.get_rel_instance_fields(rel_value)

        return data

    def get_rel_instance_fields(
        self, rel_instance: InstrumentedList[SQLModel] | SQLModel
    ) -> Dict[str, Any] | List[Dict[str, Any]] | None:
        """Get all relationship field names from a model."""
        if not rel_instance:
            return None

        # Normalize to list for unified handling
        instances = (
            rel_instance
            if isinstance(rel_instance, InstrumentedList)
            else [rel_instance]
        )
        if not instances:
            return None

        model_class = instances[0].__class__
        display_field = model_registry.get_by_model_class(model_class).display_field

        def serialize_instance(instance: SQLModel) -> Dict[str, Any] | None:
            pk_fields = get_pk_names(instance.__class__)
            if display_field:
                base = {display_field: getattr(instance, display_field)}
            else:
                base = {}
            if pk_fields:
                base.update({pk: getattr(instance, pk) for pk in pk_fields})
            return base if base else None

        result = list(v for obj in instances if (v := serialize_instance(obj)))
        return result if isinstance(rel_instance, InstrumentedList) else result[0]
