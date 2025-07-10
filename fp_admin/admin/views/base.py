from abc import ABC, abstractmethod
from typing import Any, List, Optional

from sqlmodel import SQLModel

# from fp_admin.admin.fields import FieldType  # Moved to method scope
from fp_admin.admin.fields.utils import sqlmodel_to_fieldviews
from fp_admin.admin.views.views_types import BaseView


class BaseViewFactory(ABC):
    def __init__(self, model: type[SQLModel]):
        self.model = model

    @staticmethod
    def resolve_form_type(python_type: Optional[type]) -> Any:  # FieldType at runtime
        """Map Python types to field types."""
        from fp_admin.admin.fields import FieldType

        mapping: dict[type, FieldType] = {
            str: "string",
            int: "number",
            float: "float",
            bool: "boolean",
        }
        if python_type is None:
            return "string"
        return mapping.get(python_type, "string")

    def get_fields(self) -> List[Any]:  # FieldView at runtime
        return sqlmodel_to_fieldviews(self.model)

    @abstractmethod
    def build_view(self) -> BaseView:
        pass
