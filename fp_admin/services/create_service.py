from dataclasses import dataclass
from typing import Any, Dict, Optional

from sqlmodel import Session

from fp_admin.exceptions import ModelError, ValidationError
from fp_admin.services.base import BaseService
from fp_admin.services.form_validator import FormValidator
from fp_admin.services.utils import (
    get_model_class,
    raise_serialized_validation_error,
    validate_allowed_fields,
)


@dataclass
class CreateRecordParams:
    """Parameters for create_record method."""

    data: Dict[str, Any]
    form_id: Optional[str] = None


class CreateService:
    """Service for creating model records."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.service = BaseService(session)

    def create_record(
        self,
        model_name: str,
        params: CreateRecordParams,
        include_relationships: bool = True,
    ) -> Dict[str, Any]:
        """Create a new record for a model."""
        model_class = get_model_class(model_name)

        # Validate allowed creation fields
        validate_allowed_fields(model_name, params.data, "creation")

        # Validate form data if form_id is provided
        if params.form_id:
            try:
                FormValidator.validate_and_raise(params.form_id, params.data)
            except ValidationError as e:
                field_errors = e.details.get("field_errors", {})
                raise_serialized_validation_error("Validation failed", field_errors)

        try:
            model_instance = model_class(**params.data)
            return self.service.create(
                model_instance,
                include_relationships=include_relationships,
            )
        except Exception as e:
            raise ModelError(f"Failed to create {model_name} record: {e}") from e
