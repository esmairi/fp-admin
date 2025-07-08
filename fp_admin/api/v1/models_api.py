from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlmodel import Session

from fp_admin.core import get_session
from fp_admin.schemas.base import PaginatedResponse
from fp_admin.services.models_service import GetRecordsParams, ModelService

models_api = APIRouter()


class ModelsQueryParams(BaseModel):
    """Query parameters for models API."""

    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    ids: Optional[str] = Field(
        None, description="Comma-separated list of IDs to filter by"
    )
    fields: Optional[str] = Field(
        None, description="Comma-separated list of fields to display"
    )


@models_api.get("/{model_name}", response_model=PaginatedResponse)
async def items(
    model_name: str,
    session: Session = Depends(get_session),
    params: ModelsQueryParams = Depends(),
) -> PaginatedResponse:
    service = ModelService(session)
    id_list = [int(i) for i in params.ids.split(",")] if params.ids else None
    field_list = (
        [f.strip() for f in params.fields.split(",")] if params.fields else None
    )

    get_records_params = GetRecordsParams(
        page=params.page,
        page_size=params.page_size,
        ids=id_list,
        fields=field_list,
    )

    return service.get_records(model_name, get_records_params)
