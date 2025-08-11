from typing import Any, Dict, Optional, Type

from fastapi import APIRouter, Depends
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from fp_admin.api.error_handlers import (
    handle_not_found_error,
    handle_record_error,
    handle_validation_error,
)
from fp_admin.api.v1.schemas.models import (
    ModelRecordByIdResponseSchema,
    ModelRecordsResponseSchema,
)
from fp_admin.core import get_session
from fp_admin.exceptions import NotFoundError
from fp_admin.models.views.exceptions import FpValidationErrors
from fp_admin.registry import model_registry
from fp_admin.schemas import CreateRecordParams, GetRecordsParams, UpdateRecordParams
from fp_admin.services.v1 import CreateService, ListService, ReadService, UpdateService

models_api = APIRouter()


def get_model_class(model_name: str) -> Type[SQLModel]:
    model_info = model_registry.get(model_name)
    if not model_info:
        raise handle_not_found_error("model", model_name)
    return model_info.model_class


@models_api.post(
    "/{model_name}",
    response_model=ModelRecordByIdResponseSchema,
    summary="Create model record",
    description="Create a new record for a specific model",
)
async def create_record(
    model_name: str,
    params: CreateRecordParams,
    session: AsyncSession = Depends(get_session),
) -> ModelRecordByIdResponseSchema:
    """Create a new record for a model."""
    # if not request.form_id:
    #     raise handle_validation_error()
    model_class = get_model_class(model_name)
    service = CreateService(model_class, model_name)
    try:
        created_record: Dict[str, Any] = await service.create_record(
            session, params, True
        )  # type: ignore
        return ModelRecordByIdResponseSchema(data=created_record)
    except FpValidationErrors as e:
        raise handle_validation_error(e.details) from e
    except Exception as e:
        raise handle_record_error(
            f"Failed to create {model_name} record: {str(e)}"
        ) from e


@models_api.get(
    "/{model_name}",
    response_model=ModelRecordsResponseSchema,
    summary="Get model records",
    description="Retrieve paginated records for a specific model",
)
async def items(
    model_name: str,
    session: AsyncSession = Depends(get_session),
    page: int = 1,
    page_size: int = 20,
    fields: Optional[str] = None,
) -> ModelRecordsResponseSchema:
    """Get paginated records for a model."""

    # Parse fields parameter
    field_list = [f.strip() for f in fields.split(",")] if fields else None

    params = GetRecordsParams(
        page=page,
        page_size=page_size,
        fields=field_list,
    )

    model_class = get_model_class(model_name)
    service = ListService(model_class, model_name)

    result = await service.list(session, params)

    # Convert to our schema format
    return ModelRecordsResponseSchema(
        data=result.data,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
        total_pages=result.total_pages,
        has_next=result.has_next,
        has_prev=result.has_prev,
    )


@models_api.get(
    "/{model_name}/{record_id}",
    response_model=ModelRecordByIdResponseSchema,
    summary="Get record by ID",
    description="Retrieve a single record by its ID",
)
async def get_record_by_id(
    model_name: str,
    record_id: int,
    session: AsyncSession = Depends(get_session),
    fields: Optional[str] = None,
) -> ModelRecordByIdResponseSchema:
    """Get a single record by ID."""

    # Parse fields parameter
    field_list = [f.strip() for f in fields.split(",")] if fields else None
    model_class = get_model_class(model_name)
    service = ReadService(model_class, model_name)

    try:
        record = await service.get_record_by_id(
            session,
            record_id=record_id,
            fields=field_list,
        )
    except NotFoundError as e:
        raise handle_not_found_error("record", str(record_id)) from e
    except Exception as e:
        raise handle_record_error(
            f"Failed to get {model_name} record {record_id}: {str(e)}"
        ) from e
    return ModelRecordByIdResponseSchema(data=record)  # type: ignore


@models_api.put(
    "/{model_name}/{record_id}",
    response_model=ModelRecordByIdResponseSchema,
    summary="Update model record",
    description="Update an existing record by its ID",
)
async def update_record(
    model_name: str,
    record_id: int,
    request: UpdateRecordParams,
    session: AsyncSession = Depends(get_session),
) -> ModelRecordByIdResponseSchema:
    """Update an existing record by ID."""
    params = UpdateRecordParams(data=request.data, form_id=request.form_id)
    model_class = get_model_class(model_name)
    service = UpdateService(model_class, model_name)

    try:
        updated_record = await service.update_record(session, record_id, params)
        return ModelRecordByIdResponseSchema(data=updated_record)
    except FpValidationErrors as e:
        raise handle_validation_error(e.details) from e
    except NotFoundError as e:
        raise handle_not_found_error(*e.details) from e
    except Exception as e:
        raise handle_record_error(
            f"Failed to update {model_name} record {record_id}: {str(e)}"
        ) from e
