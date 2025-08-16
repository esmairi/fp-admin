from typing import TYPE_CHECKING, List, Optional, Tuple, Type

from pydantic import BaseModel
from sqlmodel import SQLModel

from fp_admin.admin.models.helpers import get_model_relationship_fields
from fp_admin.models.field.constants import RELATIONSHIP_FIELD_TYPES

from ._view_registry import view_registry

if TYPE_CHECKING:
    from fp_admin.models.field import FpField


EXCLUDED_VIEW_FIELD_TYPES = {"password"}


class AdminModelConfig(BaseModel):
    model_class: Type[SQLModel]
    name: str
    label: str
    app: str
    relationship_fields: List[str]
    direct_fields: List[str]
    display_field: Optional[str] = None
    primary_keys: Optional[List[str]] = None

    def get_fields_by_names_and_form_id(
        self, field_names: List[str], form_id: str
    ) -> Tuple[List[str], List[str]]:
        relative_fields_names = self.get_view_relationship_fields_names(form_id)
        target_relative_field_names = [
            field_name
            for field_name in relative_fields_names
            if field_name in field_names
        ]
        direct_fields = [
            field_name
            for field_name in field_names
            if field_name not in target_relative_field_names
        ]
        return direct_fields, target_relative_field_names

    def get_fields_by_names(
        self, field_names: List[str]
    ) -> Tuple[List[str], List[str]]:
        relative_fields_names = get_model_relationship_fields(self.model_class)
        target_relative_field_names = [
            field_name
            for field_name in relative_fields_names
            if field_name in field_names
        ]
        direct_fields = [
            field_name
            for field_name in field_names
            if field_name not in target_relative_field_names
        ]
        return direct_fields, target_relative_field_names

    def get_view_excluded_field_names(self) -> List[str]:
        fields = view_registry.get_fields(self.name)
        return [
            field.name
            for field in fields
            if field.field_type in EXCLUDED_VIEW_FIELD_TYPES
        ]

    def get_view_field_names(
        self,
        exclude_sensitive: bool = True,
    ) -> List[str]:
        fields = view_registry.get_fields(self.name)

        def is_excluded(field: "FpField") -> bool:
            if exclude_sensitive:
                return field.field_type in EXCLUDED_VIEW_FIELD_TYPES
            return False

        return [field.name for field in fields if not is_excluded(field)]

    def get_view_relationship_fields(self, form_id: str) -> List["FpField"]:
        fields = view_registry.get_fields(self.name, form_id)
        return [
            field for field in fields if field.field_type in RELATIONSHIP_FIELD_TYPES
        ]

    def get_view_relationship_fields_names(self, form_id: str) -> List[str]:
        return [f.name for f in self.get_view_relationship_fields(form_id)]
