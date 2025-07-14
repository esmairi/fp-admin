from dataclasses import dataclass
from typing import Any, Dict, Optional, Type

from sqlmodel import Session, SQLModel

from fp_admin.exceptions import ModelError, ValidationError
from fp_admin.services.base import BaseService
from fp_admin.services.form_validator import FormValidator
from fp_admin.services.utils import (
    get_model_class,
    raise_serialized_validation_error,
    validate_allowed_fields,
)


@dataclass
class UpdateRecordParams:
    """Parameters for update_record method."""

    data: Dict[str, Any]
    form_id: Optional[str] = None


class UpdateService:
    """Service for updating model records."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.service = BaseService(session)

    def _update_record_fields(self, record: Any, data: Dict[str, Any]) -> None:
        """Update record fields with provided data."""
        for field, value in data.items():
            if hasattr(record, field):
                setattr(record, field, value)

    def _validate_form_data_with_existing_record(
        self,
        model_class: Type[SQLModel],
        record_id: int,
        form_id: str,
        params_data: Dict[str, Any],
    ) -> None:
        """Validate form data with existing record data merged."""
        existing_record = self.service.get_by_id(model_class, record_id)
        if not existing_record:
            raise ModelError(f"Record with ID {record_id} not found")

        existing_data = self.service.serialize(
            existing_record, include_relationships=False
        )
        validation_data = {**existing_data, **params_data}
        FormValidator.validate_and_raise(form_id, validation_data)

    def update_record(
        self,
        model_name: str,
        record_id: int,
        params: UpdateRecordParams,
        include_relationships: bool = True,
    ) -> Dict[str, Any]:
        """Update an existing record for a model."""
        model_class = get_model_class(model_name)

        # Validate allowed update fields
        validate_allowed_fields(model_name, params.data, "update")

        # Validate form data if form_id is provided
        if params.form_id:
            try:
                self._validate_form_data_with_existing_record(
                    model_class, record_id, params.form_id, params.data
                )
            except ValidationError as e:
                field_errors = e.details.get("field_errors", {})
                raise_serialized_validation_error("Validation failed", field_errors)

        try:
            existing_record = self.service.get_by_id(model_class, record_id)
            if not existing_record:
                raise ModelError(f"Record with ID {record_id} not found")

            self._update_record_fields(existing_record, params.data)
            return self.service.update_with_serialization(
                existing_record,
                include_relationships=include_relationships,
            )
        except ModelError:
            raise
        except Exception as e:
            raise ModelError(f"Failed to update {model_name} record: {e}") from e
