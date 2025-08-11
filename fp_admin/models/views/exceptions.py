from typing import List, Optional

from pydantic import BaseModel


class FieldErrorDetail(BaseModel):
    field_name: str
    code: str
    message: Optional[str] = None


class FpValidationErrors(Exception):
    def __init__(self, details: List[FieldErrorDetail]):
        self.details = details


class FpValidationError(Exception):
    def __init__(self, details: FieldErrorDetail):
        self.details = details
