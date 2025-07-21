from typing import Optional

from fastapi import APIRouter, Depends
from sqlmodel import Session

from fp_admin.api.error_handlers import (
    handle_model_error,
    handle_not_found_error,
    handle_validation_error,
)
from fp_admin.api.v1.schemas.models import (
    CreateRecordRequestSchema,
    ModelRecordByIdResponseSchema,
    ModelRecordsResponseSchema,
    UpdateRecordRequestSchema,
)
from fp_admin.core import get_session
from fp_admin.exceptions import ModelError, ValidationError
from fp_admin.services import (
    CreateRecordParams,
    GetRecordsParams,
    ModelService,
    UpdateRecordParams,
)

models_api = APIRouter()


@models_api.get(
    "/{model_name}",
    response_model=ModelRecordsResponseSchema,
    summary="Get model records",
    description="Retrieve paginated records for a specific model",
)
async def items(
    model_name: str,
    session: Session = Depends(get_session),
    page: int = 1,
    page_size: int = 20,
    fields: Optional[str] = None,
) -> ModelRecordsResponseSchema:
    """Get paginated records for a model."""
    service = ModelService(session)

    # Parse fields parameter
    field_list = [f.strip() for f in fields.split(",")] if fields else None

    params = GetRecordsParams(
        page=page,
        page_size=page_size,
        fields=field_list,
    )

    result = service.get_records(model_name, params)

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


@models_api.post(
    "/{model_name}",
    response_model=ModelRecordByIdResponseSchema,
    summary="Create model record",
    description="Create a new record for a specific model",
)
async def create_record(
    model_name: str,
    request: CreateRecordRequestSchema,
    session: Session = Depends(get_session),
) -> ModelRecordByIdResponseSchema:
    """Create a new record for a model."""
    service = ModelService(session)

    params = CreateRecordParams(data=request.data, form_id=request.form_id)

    try:
        created_record = service.create_record(model_name, params)
        return ModelRecordByIdResponseSchema(data=created_record)
    except ValidationError as e:
        raise handle_validation_error(e) from e
    except ModelError as e:
        # Handle other ModelError cases
        raise handle_model_error(
            f"Failed to create {model_name} record: {str(e)}"
        ) from e
    except Exception as e:
        raise handle_model_error(
            f"Failed to create {model_name} record: {str(e)}"
        ) from e


@models_api.put(
    "/{model_name}/{record_id}",
    response_model=ModelRecordByIdResponseSchema,
    summary="Update model record",
    description="Update an existing record by its ID",
)
async def update_record(
    model_name: str,
    record_id: int,
    request: UpdateRecordRequestSchema,
    session: Session = Depends(get_session),
) -> ModelRecordByIdResponseSchema:
    """Update an existing record by ID."""
    service = ModelService(session)

    params = UpdateRecordParams(data=request.data, form_id=request.form_id)

    try:
        updated_record = service.update_record(model_name, record_id, params)
        return ModelRecordByIdResponseSchema(data=updated_record)
    except ValidationError as e:
        # Handle validation errors with standardized error response
        raise handle_validation_error(e) from e
    except ModelError as e:
        # Handle other ModelError cases
        raise handle_model_error(
            f"Failed to update {model_name} record {record_id}: {str(e)}"
        ) from e
    except Exception as e:
        raise handle_model_error(
            f"Failed to update {model_name} record {record_id}: {str(e)}"
        ) from e


@models_api.get(
    "/{model_name}/{record_id}",
    response_model=ModelRecordByIdResponseSchema,
    summary="Get record by ID",
    description="Retrieve a single record by its ID",
)
async def get_record_by_id(
    model_name: str,
    record_id: int,
    session: Session = Depends(get_session),
    fields: Optional[str] = None,
) -> ModelRecordByIdResponseSchema:
    """Get a single record by ID."""
    service = ModelService(session)

    # Parse fields parameter
    field_list = [f.strip() for f in fields.split(",")] if fields else None

    record = service.get_record_by_id(
        model_name=model_name,
        record_id=record_id,
        fields=field_list,
    )

    if record is None:
        raise handle_not_found_error("record", str(record_id))

    return ModelRecordByIdResponseSchema(data=record)
