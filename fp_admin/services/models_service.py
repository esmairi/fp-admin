from dataclasses import dataclass
from typing import Dict, List, Optional, Union, cast

from sqlmodel import Session

from fp_admin.admin.models import model_registry
from fp_admin.exceptions import ModelError
from fp_admin.schemas.base import PaginatedResponse
from fp_admin.services import BaseService


@dataclass
class GetRecordsParams:
    """Parameters for get_records method."""

    page: int = 1
    page_size: int = 20
    ids: Optional[List[int]] = None
    fields: Optional[List[str]] = None


class ModelService:
    def __init__(self, session: Session) -> None:
        self.service = BaseService(session)

    def get_records(
        self,
        model_name: str,
        params: GetRecordsParams,
    ) -> PaginatedResponse:
        model_class = model_registry.get_model_class(model_name)
        if not model_class:
            raise ModelError(f"Model [{model_name}] not found in registry")

        filters = None
        if params.ids:
            filters = cast(
                Dict[str, Union[str, List[str], List[int]]], {"id": params.ids}
            )

        from fp_admin.services.base import GetAllParams

        get_all_params = GetAllParams(
            page=params.page,
            page_size=params.page_size,
            filters=filters,
            fields=params.fields,
        )

        items, total = self.service.get_all(model_class, get_all_params)
        total_pages = (total + params.page_size - 1) // params.page_size if total else 1
        return PaginatedResponse(
            data=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_prev=params.page > 1,
        )
