"""
Models API schemas for fp-admin.

This module provides serialization schemas for the models API endpoints.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema class with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        extra="forbid",
        str_strip_whitespace=True,
    )


class CreateRecordRequestSchema(BaseSchema):
    """Schema for create record request."""

    data: Dict[str, Any]
    form_id: Optional[str] = None


class UpdateRecordRequestSchema(BaseSchema):
    """Schema for update record request."""

    data: Dict[str, Any]
    form_id: Optional[str] = None


class ModelRecordByIdResponseSchema(BaseSchema):
    """Schema for model record by ID response."""

    data: Dict[str, Any]


class ModelRecordsResponseSchema(BaseSchema):
    """Schema for paginated model records response."""

    data: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class ModelQueryParamsSchema(BaseModel):
    """Schema for model query parameters."""

    page: int = 1
    page_size: int = 20
    fields: Optional[str] = None
    filters: Optional[str] = None
    include: Optional[str] = None
