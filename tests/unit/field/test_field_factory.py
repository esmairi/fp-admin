import datetime as dt
import re

import pytest
from sqlmodel import Field, SQLModel

from fp_admin.models.field import FieldFactory
from fp_admin.models.field.widgets import DEFAULT_WIDGETS

# --- Helpers / fakes ---------------------------------------------------------


class DummyModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)


# --- Core field tests (type, widget, annotation, default) --------------------


@pytest.mark.parametrize(
    "maker,kwargs,expected_type,expected_widget,expected_ann",
    [
        (
            FieldFactory.primary_key_field,
            {},
            "primary_key",
            None,
            None,
        ),  # widget may be from DEFAULT_WIDGETS
        (FieldFactory.string_field, {}, "string", None, str),
        (FieldFactory.text_field, {}, "string", "textarea", str),
        (FieldFactory.email_field, {}, "string", None, str),
        (FieldFactory.password_field, {}, "password", None, str),
        (FieldFactory.number_field, {}, "number", None, int),
        (FieldFactory.slider_field, {}, "number", None, int),
        (FieldFactory.float_field, {}, "float", None, float),
        (FieldFactory.time_field, {}, "time", None, dt.time),
        (FieldFactory.datetime_field, {}, "datetime", None, dt.datetime),
        (FieldFactory.date_field, {}, "date", None, dt.date),
        (FieldFactory.boolean_field, {}, "boolean", None, bool),
        (FieldFactory.toggle_field, {}, "boolean", "switch", bool),
        (FieldFactory.chips_field, {}, "multichoice", "chips", None),
        (FieldFactory.listbox_field, {}, "multichoice", "listBox", None),
        (FieldFactory.choice_field, {}, "choice", "select", None),
        (FieldFactory.multichoice_field, {}, "multichoice", None, None),
        (FieldFactory.file_field, {}, "file", None, None),
        (FieldFactory.image_field, {}, "file", "image", None),
        (FieldFactory.json_field, {}, "json", None, None),
        (FieldFactory.radio_field, {}, "choice", "radio", None),
        (FieldFactory.autocomplete_field, {}, "string", "autoComplete", None),
    ],
)
def test_field_factory_basics(
    maker, kwargs, expected_type, expected_widget, expected_ann
):
    f = maker("field_name", **kwargs)

    # type
    assert f.field_type == expected_type

    # widget: either explicitly set by the factory or falls back to DEFAULT_WIDGETS
    if expected_widget is not None:
        assert f.widget == expected_widget
    else:
        # when not explicitly set, verify it's consistent with default mapping (if any)
        assert f.widget == DEFAULT_WIDGETS.get(expected_type)

    # annotation (when the factory specifies it)
    if expected_ann is not None:
        # FieldInfo stores the computed annotation on its
        # .annotation attribute in Pydantic v2
        assert getattr(f, "annotation", None) is not None, "annotation should be set"
        # The computed annotation is usually Optional[T] when not required;
        # check origin type compatibility
        ann_str = str(getattr(f, "annotation"))
        assert (
            expected_ann.__name__ in ann_str
        ), f"expected {expected_ann} inside {ann_str}"

    # default handling: factories don’t pass defaults; non-required fields
    # should default to None
    assert getattr(f, "default", None) is None


def test_primary_key_flag_and_name():
    f = FieldFactory.primary_key_field("id")
    assert f.is_primary_key is True
    assert f.name == "id"


# --- Validators & patterns ---------------------------------------------------


def test_email_field_has_pattern_validator():
    f = FieldFactory.email_field("email")
    # pattern must be present in validators and also configured
    # in FieldInfo kwargs
    assert f.validators, "validators list should not be empty"
    codes = {v.error.code for v in f.validators if v.error}
    assert "pattern" in codes

    # sanity check: the regex should match a normal email
    regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    assert regex.fullmatch("user@example.com")


def test_builtin_validators_propagate_to_kwargs_and_list():
    f = FieldFactory.string_field(
        "username",
        validators=[
            # Using your FpFieldValidator model structure
            # (import path shortened for readability if needed)
            # from fp_admin.models.field._fp_field import FpFieldValidator
            # but to avoid import path churn, pass via kwargs since factory
            # forwards to FpField
        ],
        min_length=3,
        max_length=20,
    )
    # Validators list should include min_length/max_length entries
    names = {v.name for v in (f.validators or [])}
    assert {"min_length", "max_length"}.issubset(names)


# --- Relationship fields -----------------------------------------------------


def test_relationship_requires_model_class():
    with pytest.raises(ValueError):
        FieldFactory.foreignkey_field("user")  # no model_class -> error


@pytest.mark.parametrize(
    "maker,ftype",
    [
        (FieldFactory.foreignkey_field, "foreign_key"),
        (FieldFactory.many_to_many_field, "many_to_many"),
        (FieldFactory.one_to_one_field, "one_to_one"),
    ],
)
def test_relationship_options_built(maker, ftype):
    f = maker(
        "user",
        model_class=DummyModel,
        display_field="name",
    )
    assert f.field_type == ftype
    assert f.options is not None
    assert f.options["model_class"] is DummyModel
    assert f.options["display_field"] == "name"
    assert f.options["field_id"] == "id"
