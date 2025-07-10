from typing import Any, Dict, List, Optional

from sqlmodel import Session

from fp_admin.schemas.base import PaginatedResponse
from fp_admin.services.create_service import CreateRecordParams, CreateService
from fp_admin.services.read_service import (
    GetRecordsParams,
    ReadService,
)
from fp_admin.services.update_service import (
    UpdateRecordParams,
    UpdateService,
)


class ModelService:
    """Unified service for model operations combining
    read, create, and update services."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.read_service = ReadService(session)
        self.create_service = CreateService(session)
        self.update_service = UpdateService(session)

    def get_records(
        self,
        model_name: str,
        params: GetRecordsParams,
    ) -> PaginatedResponse:
        """Get paginated records for a model."""
        return self.read_service.get_records(model_name, params)

    def get_record_by_id(
        self,
        model_name: str,
        record_id: int,
        fields: Optional[List[str]] = None,
        include_relationships: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """Get a single record by ID."""
        return self.read_service.get_record_by_id(
            model_name, record_id, fields, include_relationships
        )

    def create_record(
        self,
        model_name: str,
        params: CreateRecordParams,
        include_relationships: bool = True,
    ) -> Dict[str, Any]:
        """Create a new record for a model."""
        return self.create_service.create_record(
            model_name, params, include_relationships
        )

    def update_record(
        self,
        model_name: str,
        record_id: int,
        params: UpdateRecordParams,
        include_relationships: bool = True,
    ) -> Dict[str, Any]:
        """Update an existing record for a model."""
        return self.update_service.update_record(
            model_name, record_id, params, include_relationships
        )
