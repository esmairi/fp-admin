from typing import Any, Callable, Dict, List, Literal, Optional

from pydantic import BaseModel

from fp_admin.admin.fields import FieldError, FieldView


class BaseView(BaseModel):
    name: str
    view_type: Literal["form", "list"]
    model: str
    fields: List[FieldView]
    default_form_id: Optional[str] = None
    creation_fields: Optional[List[str]] = None
    allowed_update_fields: Optional[List[str]] = None


class FormView(BaseView):
    view_type: Literal["form"] = "form"
    validate_form: Optional[Callable[[Dict[str, Any]], List[FieldError]]] = None


class ListView(BaseView):
    view_type: Literal["list"] = "list"
