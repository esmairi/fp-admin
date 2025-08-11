"""
Schemas package for fp-admin.

This package contains Pydantic schemas for request/response validation
and data serialization.
"""

from .base import (
    CreateRecordParams,
    GetRecordsParams,
    PaginatedResponse,
    UpdateRecordParams,
)

__all__ = [
    "CreateRecordParams",
    "GetRecordsParams",
    "UpdateRecordParams",
    "PaginatedResponse",
]
