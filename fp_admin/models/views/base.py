from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Literal, Optional, Type

from pydantic import BaseModel, ValidationError, create_model
from sqlmodel import SQLModel

from .exceptions import FieldErrorDetail, FpValidationErrors

if TYPE_CHECKING:
    from fp_admin.models.field import FieldError, FpField


@dataclass
class BaseView:  # pylint: disable=R0902
    name: str
    model: Type[SQLModel]
    view_type: Literal["form", "list"] = "form"
    fields: List["FpField"] = field(default_factory=list)
    default_form_id: Optional[str] = None
    creation_fields: List[str] = field(default_factory=list)
    allowed_update_fields: List[str] = field(default_factory=list)
    display_fields: List[str] = field(default_factory=list)

    def get_field(self, name: str) -> "FpField":
        if self.fields:
            fds = [f for f in self.fields if f.name == name]
            if fds:
                return fds[0]
        raise ValidationError(f"Field {name} not found.")


class FormView(BaseView):

    view_type: Literal["form"] = "form"
    validate_form: Optional[Callable[[Dict[str, Any]], List["FieldError"]]] = None

    def validate_create_fields(self, data: Dict[str, Any]) -> None:
        self.validate_fields(self.creation_fields, data)

    def validate_fields(self, fields: List[str], data: Dict[str, Any]) -> None:
        _FormModel = self.build_model_from_fields(fields)  # pylint: disable=C0103
        if not _FormModel:
            return None
        try:
            _FormModel.model_validate(data)
        except ValidationError as e:
            self.raise_validation_error(e)
        return None

    def build_model_from_fields(
        self, model_fields: List[str]
    ) -> Type[BaseModel] | None:
        if not model_fields or not self.fields:
            return None

        create_fields_obj = [f for f in self.fields if f.name in model_fields]

        create_fields = {f.name: (f.annotation, f) for f in create_fields_obj}

        if create_fields:
            return create_model(f"__{self.name}", **create_fields)  # type: ignore
        return None

    def raise_validation_error(self, validation_error: ValidationError) -> None:
        formatted_errors = []
        for err in validation_error.errors():
            field_name = ".".join(map(str, err["loc"]))
            err_type = err["type"]
            field_obj = self.get_field(field_name)
            validatior = field_obj.get_validator_by_error_code(err_type)
            if validatior:
                err_code = validatior.error.code if validatior.error else err_type
                err_msg = validatior.error.message if validatior.error else err["msg"]
                formatted_errors.append(
                    FieldErrorDetail(
                        code=err_code, message=err_msg, field_name=field_name
                    )
                )
                continue
            formatted_errors.append(
                FieldErrorDetail(
                    code=err_type, message=err["msg"], field_name=field_name
                )
            )
        raise FpValidationErrors(formatted_errors)

    def validate_update_fields(self, data: Dict[str, Any]) -> None:
        self.validate_fields(self.allowed_update_fields, data)


class ListView(BaseView):
    view_type: Literal["list"] = "list"


class BaseViewFactory(ABC):
    def __init__(self, model: type[SQLModel]):
        self.model = model

    def get_fields(self) -> List[Any]:
        return []

    @abstractmethod
    def build_view(self) -> BaseView:
        pass


class FormViewFactory(BaseViewFactory):
    def build_view(self) -> FormView:
        return FormView(
            name=f"{self.model.__name__}Form",
            model=self.model,
            fields=self.get_fields(),
        )


class ListViewFactory(BaseViewFactory):
    def build_view(self) -> ListView:
        return ListView(
            name=f"{self.model.__name__}List",
            model=self.model,
            default_form_id=f"{self.model.__name__}Form",
            fields=self.get_fields(),
        )
