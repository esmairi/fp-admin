"""
Views API schemas for fp-admin.

This module provides serialization schemas for the views API endpoints.
"""

from typing import Any, Dict, List, Literal, Optional, Type, Union

from pydantic import BaseModel, ConfigDict, Field, field_serializer
from sqlmodel import SQLModel

from fp_admin.exceptions import ViewError
from fp_admin.models.field import FpFieldValidator
from fp_admin.models.views import BaseView

BaseViewInstanceSchema = Union["FormViewSchema", "ListViewSchema"]


class FieldErrorResponse(BaseModel):
    """Schema for field error information."""

    code: str
    message: Optional[str] = None
    field_name: str


class WidgetConfig(BaseModel):
    """Configuration options for widgets."""


class FieldViewSchema(BaseModel):
    """Schema for serializing FieldView objects."""

    model_config = ConfigDict(from_attributes=True)
    # pylint: disable=R0801

    name: str
    field_type: str
    title: Optional[str] = None
    help_text: Optional[str] = None
    widget: Optional[str] = None
    required: bool = False
    readonly: bool = False
    disabled: bool = False
    placeholder: Optional[str] = None
    default: Optional[Any] = None
    options: Optional[Dict[str, Any]] = None
    validators: List[FpFieldValidator] = Field(default_factory=list)
    is_primary_key: bool = False
    display_field: str | None
    # pylint: enable=R0801

    @field_serializer("options", when_used="always")
    def serialize_options(
        self, options: Dict[str, Any] | None
    ) -> Dict[str, Any] | None:
        # Convert the SQLModel subclass (class object) into its class name
        if options and options.get("model_class"):
            options["model"] = str(getattr(options["model_class"], "__name__")).lower()
            del options["model_class"]
        return options


class BaseViewSchema(BaseModel):
    """Schema for serializing BaseView objects."""

    model_config = ConfigDict(from_attributes=True)

    name: str
    view_type: Literal["form", "list"]
    model: Type[SQLModel]
    fields: List[FieldViewSchema]
    default_form_id: Optional[str] = None

    @field_serializer("model", when_used="always")
    def serialize_model(self, model: Any) -> str:
        # Convert the SQLModel subclass (class object) into its class name
        return str(getattr(model, "__name__")).lower()

    @classmethod
    def serialize_view(cls, view: "BaseView") -> "BaseViewInstanceSchema":
        """Serialize a view object to the appropriate schema based on its type."""
        if view.view_type == "form":
            return FormViewSchema.model_validate(view)
        if view.view_type == "list":
            return ListViewSchema.model_validate(view)
        raise ViewError("view type not supported")


class FormViewSchema(BaseViewSchema):
    """Schema for serializing FormView objects."""

    view_type: Literal["form"] = "form"
    creation_fields: List[str] = Field(default_factory=list)
    allowed_update_fields: List[str] = Field(default_factory=list)


class ListViewSchema(BaseViewSchema):
    """Schema for serializing ListView objects."""

    view_type: Literal["list"] = "list"


class ViewsResponseSchema(BaseModel):
    """Schema for the response of all views endpoint."""

    data: Dict[str, List[BaseViewInstanceSchema]]


class ModelViewsResponseSchema(BaseModel):
    """Schema for the response of model views endpoint."""

    data: List[BaseViewInstanceSchema]
