from typing import (
    Any,
    List,
    NotRequired,
    Optional,
    Type,
    TypedDict,
    Unpack,
)

from pydantic import BaseModel
from pydantic.fields import FieldInfo, _FieldInfoInputs
from sqlmodel import SQLModel

from fp_admin.admin.models import get_pk_names

from .constants import RELATIONSHIP_FIELD_TYPES, FieldType
from .widgets import DEFAULT_WIDGETS, WidgetType


class FpFieldOption(TypedDict, total=False):
    field_id: str | int
    display_field: str | None
    model_class: Type[SQLModel]
    choices: List[Any]


class FpFieldError(BaseModel):
    code: str
    message: Optional[str] = None


class FpFieldValidator(BaseModel):
    name: str
    condition_value: Any
    error: Optional[FpFieldError] = None


class _FpFieldInfoInputs(_FieldInfoInputs):
    help_text: NotRequired[str]
    display_field: NotRequired[str]
    model_class: NotRequired[Type[SQLModel]]
    widget: NotRequired[WidgetType]
    required: NotRequired[bool]
    readonly: NotRequired[bool]
    disabled: NotRequired[bool]
    placeholder: NotRequired[str]
    options: NotRequired[FpFieldOption]
    validators: NotRequired[List[FpFieldValidator]]
    custom_validator: NotRequired[Any]
    is_primary_key: NotRequired[bool]


class FpField(FieldInfo):  # pylint: disable=R0902
    name: str
    field_type: FieldType
    help_text: str | None
    widget: WidgetType | None
    required: bool | None
    readonly: bool | None
    disabled: bool | None
    placeholder: str | None
    options: FpFieldOption | None
    validators: List[FpFieldValidator] | None
    custom_validator: Any | None
    is_primary_key: bool

    __slots__ = (
        *FieldInfo.__slots__,
        "name",
        "field_type",
        "help_text",
        "widget",
        "required",
        "readonly",
        "disabled",
        "placeholder",
        "options",
        "validators",
        "custom_validator",
        "is_primary_key",
    )

    @property
    def model_class(self) -> Type[SQLModel]:
        return self.options.get("model_class", SQLModel) if self.options else SQLModel

    @property
    def display_field(self) -> str | None:
        return self.options.get("display_field") if self.options else None

    def __init__(
        self,
        name: str,
        field_type: FieldType,
        **kwargs: Unpack[_FpFieldInfoInputs],
    ):
        kwargs = self._set_validators_from_kwargs(**kwargs)
        help_text = kwargs.pop("help_text", None)
        widget = kwargs.pop("widget", None)
        required = kwargs.pop("required", False)
        readonly = kwargs.pop("readonly", False)
        disabled = kwargs.pop("disabled", False)
        placeholder = kwargs.pop("placeholder", None)
        custom_validator = kwargs.pop("custom_validator", None)
        is_primary_key = kwargs.pop("is_primary_key", False)

        # check RELATIONSHIP_FIELD

        if not field_type:
            raise AttributeError("field_type must be specified")
        if "annotation" in kwargs:
            if not required:
                kwargs["annotation"] = kwargs["annotation"] | None  # type: ignore
        else:
            kwargs["annotation"] = Any
        if not kwargs.get("default") and not required:
            kwargs["default"] = None
        options = self._get_field_options(field_type, name, **kwargs)
        super().__init__(**kwargs)
        self.name = name
        self.help_text = help_text
        self.field_type = field_type
        self.widget = widget or DEFAULT_WIDGETS.get(field_type)
        self.required = required
        self.readonly = readonly
        self.disabled = disabled
        self.placeholder = placeholder
        self.options = options
        self.custom_validator = custom_validator
        self.is_primary_key = is_primary_key

    def _set_validators_from_kwargs(
        self, **kwargs: Unpack[_FpFieldInfoInputs]
    ) -> _FpFieldInfoInputs:
        validators: List[FpFieldValidator] = kwargs.pop("validators", []) or []
        builtin_validators = [
            "gt",
            "ge",
            "lt",
            "le",
            "multiple_of",
            "min_length",
            "max_length",
            "pattern",
        ]
        for v in validators:
            if v.name in builtin_validators:
                kwargs[v.name] = v.condition_value  # type: ignore

        self.validators = validators + [
            FpFieldValidator(
                name=k,
                condition_value=kwargs.get(k),
                error=FpFieldError(code=k),
            )
            for k in builtin_validators
            if kwargs.get(k)
        ]
        return kwargs

    def get_validator_by_error_code(self, error_code: str) -> FpFieldValidator | None:
        vs = self.validators or []
        target_v = [v for v in vs if v.error and v.error.code == error_code]
        return target_v[0] if target_v else None

    def _get_field_options(
        self, field_type: FieldType, name: str, **kwargs: Unpack[_FpFieldInfoInputs]
    ) -> FpFieldOption | None:
        display_field = kwargs.pop("display_field", None)
        model_class = kwargs.pop("model_class", None)
        options = kwargs.pop("options", None)

        if field_type in RELATIONSHIP_FIELD_TYPES:
            if not model_class:
                raise AttributeError(
                    f"model_class is required with field_type: "
                    f"{field_type} , field name: {name}"
                )
            options = options or {}
            options.update(
                {
                    "field_id": ",".join(get_pk_names(model_class)),
                    "display_field": display_field,
                    "model_class": model_class,
                }
            )
        return options
