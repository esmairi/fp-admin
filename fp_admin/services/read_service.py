from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from sqlmodel import Session

from fp_admin.schemas.base import PaginatedResponse
from fp_admin.services.base import BaseService, GetAllParams
from fp_admin.services.utils import get_model_class


@dataclass
class GetRecordsParams:
    """Parameters for get_records method."""

    page: int = 1
    page_size: int = 20
    ids: Optional[List[int]] = None
    fields: Optional[List[str]] = None
    include: Optional[List[str]] = None


class ReadService:
    """Service for reading/fetching model records."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.service = BaseService(session)

    def get_records(
        self,
        model_name: str,
        params: GetRecordsParams,
    ) -> PaginatedResponse:
        """Get paginated records for a model."""
        model_class = get_model_class(model_name)

        get_all_params = GetAllParams(
            page=params.page,
            page_size=params.page_size,
            filters={"id": params.ids} if params.ids else None,
            fields=params.fields,
            include_relationships=True,
            include=params.include,
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

    def get_record_by_id(
        self,
        model_name: str,
        record_id: int,
        fields: Optional[List[str]] = None,
        include_relationships: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """Get a single record by ID."""
        model_class = get_model_class(model_name)

        return self.service.get_by_id_with_fields(
            model_class,
            record_id,
            fields=fields,
            include_relationships=include_relationships,
        )

    def search_records(self, model_name: str, **filters: Any) -> List[Dict[str, Any]]:
        """Search records for a model."""
        model_class = get_model_class(model_name)
        return self.service.filter(model_class, **filters)
