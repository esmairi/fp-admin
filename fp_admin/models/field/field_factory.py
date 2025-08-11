import datetime
from typing import Unpack

from ._fp_field import FpField, _FpFieldInfoInputs
from .constants import FieldType


class FieldFactory:  # pylint: disable=R0904

    @classmethod
    def primary_key_field(
        cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]
    ) -> FpField:
        """Create a primary  field."""
        return FpField(name, "primary_key", is_primary_key=True, **kwargs)

    @classmethod
    def string_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return FpField(name, "string", annotation=str, **kwargs)

    @classmethod
    def text_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a text area  field."""
        return FpField(name, "string", widget="textarea", annotation=str, **kwargs)

    @classmethod
    def email_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create an email input field."""
        return FpField(
            name=name,
            field_type="string",
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            annotation=str,
            **kwargs,
        )

    @classmethod
    def password_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return FpField(name=name, field_type="password", annotation=str, **kwargs)

    @classmethod
    def number_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return FpField(name=name, annotation=int, field_type="number", **kwargs)

    @classmethod
    def slider_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return cls.number_field(name=name, **kwargs)

    @classmethod
    def float_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return FpField(name=name, annotation=float, field_type="float", **kwargs)

    @classmethod
    def time_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return FpField(name=name, field_type="time", annotation=datetime.time, **kwargs)

    @classmethod
    def datetime_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return FpField(
            name=name, field_type="datetime", annotation=datetime.datetime, **kwargs
        )

    @classmethod
    def date_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return FpField(name=name, field_type="date", annotation=datetime.date, **kwargs)

    @classmethod
    def boolean_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return FpField(name=name, field_type="boolean", annotation=bool, **kwargs)

    @classmethod
    def toggle_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return cls.boolean_field(name=name, widget="switch", **kwargs)

    @classmethod
    def chips_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return cls.multichoice_field(name=name, widget="chips", **kwargs)

    @classmethod
    def listbox_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return cls.multichoice_field(name=name, widget="listBox", **kwargs)

    @classmethod
    def choice_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return FpField(name=name, field_type="choice", widget="select", **kwargs)

    @classmethod
    def multichoice_field(
        cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]
    ) -> FpField:
        """Create a string input field."""
        return FpField(name=name, field_type="multichoice", **kwargs)

    @classmethod
    def file_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return FpField(name=name, field_type="file", **kwargs)

    @classmethod
    def image_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return cls.file_field(name=name, widget="image", **kwargs)

    @classmethod
    def json_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a string input field."""
        return FpField(name=name, field_type="json", **kwargs)

    @classmethod
    def radio_field(cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]) -> FpField:
        """Create a radio field."""
        return cls.choice_field(
            name=name,
            widget="radio",
            **kwargs,
        )

    @classmethod
    def autocomplete_field(
        cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]
    ) -> FpField:
        """Create an autocomplete field."""
        return FpField(
            name=name,
            field_type="string",
            widget="autoComplete",
            **kwargs,
        )

    @classmethod
    def _relationship_field(
        cls, name: str, field_type: FieldType, **kwargs: Unpack[_FpFieldInfoInputs]
    ) -> FpField:
        model_class = kwargs.get("model_class")
        if not model_class:
            raise ValueError("model_class is required")
        return FpField(
            name,
            field_type,
            **kwargs,
        )

    @classmethod
    def foreignkey_field(
        cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]
    ) -> FpField:
        return cls._relationship_field(name, "foreign_key", **kwargs)

    @classmethod
    def many_to_many_field(
        cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]
    ) -> FpField:
        return cls._relationship_field(name, "many_to_many", **kwargs)

    @classmethod
    def one_to_one_field(
        cls, name: str, **kwargs: Unpack[_FpFieldInfoInputs]
    ) -> FpField:
        return cls._relationship_field(name, "one_to_one", **kwargs)
