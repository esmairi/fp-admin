"""
Views API schemas for fp-admin.

This module provides serialization schemas for the views API endpoints.
"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict

from fp_admin.exceptions import ViewError

BaseViewInstanceSchema = Union["FormViewSchema", "ListViewSchema"]


class FieldErrorSchema(BaseModel):
    """Schema for field error information."""

    message: str
    code: Optional[str] = None


class WidgetConfig(BaseModel):
    """Configuration options for widgets."""


class FieldViewSchema(BaseModel):
    """Schema for serializing FieldView objects."""

    model_config = ConfigDict(from_attributes=True)
    # pylint: disable=R0801

    name: str
    title: Optional[str] = None
    help_text: Optional[str] = None
    field_type: str
    widget: Optional[str] = None
    required: bool = False
    readonly: bool = False
    disabled: bool = False
    placeholder: Optional[str] = None
    default_value: Optional[Any] = None
    options: Optional[Dict[str, Any]] = None
    error: Optional[FieldErrorSchema] = None
    # validation: Optional[FieldValidationSchema] = None
    is_primary_key: bool = False
    # pylint: enable=R0801


class BaseViewSchema(BaseModel):
    """Schema for serializing BaseView objects."""

    model_config = ConfigDict(from_attributes=True)

    name: str
    view_type: Literal["form", "list"]
    model: str
    fields: List[FieldViewSchema]
    default_form_id: Optional[str] = None

    @classmethod
    def serialize_view(cls, view: "BaseViewSchema") -> "BaseViewInstanceSchema":
        """Serialize a view object to the appropriate schema based on its type."""
        if view.view_type == "form":
            return FormViewSchema.model_validate(view)
        if view.view_type == "list":
            return ListViewSchema.model_validate(view)
        raise ViewError("view type not supported")


class FormViewSchema(BaseViewSchema):
    """Schema for serializing FormView objects."""

    view_type: Literal["form"] = "form"
    creation_fields: List[str]
    allowed_update_fields: List[str]


class ListViewSchema(BaseViewSchema):
    """Schema for serializing ListView objects."""

    view_type: Literal["list"] = "list"


class ViewsResponseSchema(BaseModel):
    """Schema for the response of all views endpoint."""

    data: Dict[str, List[BaseViewInstanceSchema]]


class ModelViewsResponseSchema(BaseModel):
    """Schema for the response of model views endpoint."""

    data: List[BaseViewInstanceSchema]
