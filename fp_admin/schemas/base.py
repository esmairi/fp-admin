"""
Base schemas for fp-admin.

This module provides base schema classes that other schemas should inherit from.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    """Base schema class with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        extra="forbid",
        str_strip_whitespace=True,
    )


class CreateRecordParams(BaseSchema):
    """Parameters for create_record method."""

    data: Dict[str, Any]
    form_id: Optional[str] = None


class UpdateRecordParams(BaseSchema):
    """Parameters for update_record method."""

    data: Dict[str, Any]
    form_id: Optional[str] = None


class GetRecordsParams(BaseModel):
    """Parameters for get_records method."""

    page: int = 1
    page_size: int = 20
    fields: Optional[List[str]] = None
    filters: Optional[List[str]] = None
    sort_by: Optional[str] = Field(default=None, description="Field to sort by")


class PaginationParams(BaseSchema):
    """Pagination parameters for list endpoints."""

    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")
    sort_by: Optional[str] = Field(default=None, description="Field to sort by")
    sort_order: str = Field(
        default="asc", pattern="^(asc|desc)$", description="Sort order"
    )


class PaginatedResponse(BaseSchema):
    """Paginated response wrapper."""

    data: List[Any] = Field(description="List of items")
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Items per page")
    total_pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Whether there is a next page")
    has_prev: bool = Field(description="Whether there is a previous page")


class ErrorResponse(BaseSchema):
    """Error response schema."""

    error: str = Field(description="Error message")
    status_code: int = Field(description="HTTP status code")
    details: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional error details"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Error timestamp"
    )
