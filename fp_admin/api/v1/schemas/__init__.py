"""
API v1 schemas for fp-admin.

This module provides serialization schemas for the API endpoints.
"""

from .models import (
    ModelQueryParamsSchema,
    ModelRecordByIdResponseSchema,
    ModelRecordsResponseSchema,
)

__all__ = [
    # Models schemas
    "ModelRecordsResponseSchema",
    "ModelRecordByIdResponseSchema",
    "ModelQueryParamsSchema",
]
