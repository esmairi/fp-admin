"""
Field factory for fp-admin.

This module provides the FieldFactory class for creating different types of form fields.
"""

from typing import Any, Callable, Optional, Type, Unpack

from sqlmodel import SQLModel

from fp_admin.exceptions import ValidationError
from fp_admin.utils.primary_key import get_primary_key_field

from .base import FieldView, FieldViewKwargs
from .errors import FieldError
from .field_validator import FieldValidation
from .widgets import WidgetConfig


class FieldFactory:  # pylint: disable=too-many-public-methods
    """Factory class for creating FieldView instances.

    This class provides static methods for creating different types of form fields.
    The high number of methods is intentional to provide a comprehensive API
    for all field types supported by fp-admin.
    """

    @classmethod
    def get_validator(cls, **kwargs: Any) -> Optional[FieldValidation]:
        """
        Build FieldValidation from kwargs that match validation parameters.

        Args:
            **kwargs: Keyword arguments that may contain validation parameters

        Returns:
            FieldValidation object if validation parameters are found, None otherwise
        """
        validation_params = {}
        # Dynamically get validation keys from FieldValidation fields
        validation_keys = FieldValidation.model_fields.keys()

        for key in validation_keys:
            if key in kwargs:
                validation_params[key] = kwargs[key]

        if validation_params:
            return FieldValidation(**validation_params)
        return None

    @classmethod
    def _filter_field_kwargs(cls, **kwargs: Any) -> dict[str, Any]:
        """Filter out validation fields from kwargs, returning only
        field-specific kwargs."""
        excluded_keys = set(FieldValidation.model_fields.keys())
        excluded_keys.add("custom_validator")  # Also exclude custom_validator
        return {k: v for k, v in kwargs.items() if k not in excluded_keys}

    @classmethod
    def _get_custom_validator(
        cls, **kwargs: Any
    ) -> Optional[Callable[[Any], Optional["FieldError"]]]:
        """Extract custom validator from kwargs."""
        return kwargs.get("custom_validator")

    @classmethod
    def string_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a string input field."""
        validation = cls.get_validator(**kwargs)
        custom_validator = cls._get_custom_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="string",
            validators=validation,
            custom_validator=custom_validator,
            **field_kwargs,
        )

    @classmethod
    def text_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a text input field (alias for string_field)."""
        return cls.string_field(name, title, **kwargs)

    @classmethod
    def email_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create an email input field."""
        validation = FieldValidation(
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )
        # Merge with any additional validation from kwargs
        additional_validation = cls.get_validator(**kwargs)
        if additional_validation:
            # Merge validation rules
            for key, value in additional_validation.model_dump().items():
                if value is not None:
                    setattr(validation, key, value)

        custom_validator = cls._get_custom_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="string",
            validators=validation,
            custom_validator=custom_validator,
            **field_kwargs,
        )

    @classmethod
    def password_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a password input field."""
        validation = cls.get_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="string",
            widget="password",
            validators=validation,
            **field_kwargs,
        )

    @classmethod
    def textarea_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a textarea field."""
        validation = cls.get_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="string",
            widget="textarea",
            validators=validation,
            **field_kwargs,
        )

    @classmethod
    def number_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a number input field."""
        validation = cls.get_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="number",
            validators=validation,
            **field_kwargs,
        )

    @classmethod
    def float_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a float input field."""
        validation = cls.get_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="float",
            validators=validation,
            **field_kwargs,
        )

    @classmethod
    def slider_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a slider field for numbers."""
        validation = cls.get_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="number",
            widget="Slider",
            validators=validation,
            **field_kwargs,
        )

    @classmethod
    def time_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a time input field."""
        # Get existing widget_config from kwargs or create new one
        existing_config = kwargs.pop("widget_config", None)
        if existing_config:
            # Merge with existing config
            if hasattr(existing_config, "timeOnly"):
                existing_config.timeOnly = True
            widget_config = existing_config
        else:
            # Create new config with timeOnly enabled
            widget_config = WidgetConfig(timeOnly=True)

        validation = cls.get_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="time",
            widget_config=widget_config,
            validators=validation,
            **field_kwargs,
        )

    @classmethod
    def datetime_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a datetime input field."""
        # Get existing widget_config from kwargs or create new one
        existing_config = kwargs.pop("widget_config", None)
        if existing_config:
            # Merge with existing config
            if hasattr(existing_config, "showTime"):
                existing_config.showTime = True
            widget_config = existing_config
        else:
            # Create new config with showTime enabled
            widget_config = WidgetConfig(showTime=True)

        validation = cls.get_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="datetime",
            widget_config=widget_config,
            validators=validation,
            **field_kwargs,
        )

    @classmethod
    def date_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a date input field."""
        validation = cls.get_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="date",
            validators=validation,
            **field_kwargs,
        )

    @classmethod
    def boolean_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a boolean field."""
        validation = cls.get_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="boolean",
            validators=validation,
            **field_kwargs,
        )

    @classmethod
    def checkbox_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a checkbox field (alias for boolean_field)."""
        return cls.boolean_field(name, title, **kwargs)

    @classmethod
    def switch_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a switch field."""
        validation = cls.get_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="boolean",
            widget="switch",
            validators=validation,
            **field_kwargs,
        )

    @classmethod
    def choice_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a choice field."""
        validation = cls.get_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="choice",
            validators=validation,
            **field_kwargs,
        )

    @classmethod
    def multichoice_field(
        cls, name: str, title: str, **kwargs: Unpack[FieldViewKwargs]
    ) -> FieldView:
        """Create a multichoice field."""
        validation = cls.get_validator(**kwargs)
        field_kwargs = cls._filter_field_kwargs(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="multichoice",
            validators=validation,
            **field_kwargs,
        )

    @classmethod
    def _build_relationship_options(
        cls, model_class: Type[SQLModel], field_title: str
    ) -> dict[str, Any]:
        """Build options for relationship fields.

        Args:
            model_class: The model class
            field_title: The field name from the model used to display records

        Returns:
            Options dictionary with field_title, field_id, and target_model

        Raises:
            ValidationError: If model_class or field_title is not provided
        """
        if not model_class:
            raise ValidationError("model_class is required for relationship fields")
        if not field_title:
            raise ValidationError("field_title is required for relationship fields")

        field_id = get_primary_key_field(model_class)

        return {
            "field_title": field_title,  # This is the field name to use for display
            "field_id": field_id,
            "target_model": model_class.__name__.lower(),
        }

    @classmethod
    def _relationship_field(
        cls, name: str, title: str, field_type: str, **kwargs: Any
    ) -> FieldView:
        model_class = kwargs.pop("model_class", None)
        field_title = kwargs.pop("field_title", None)
        options = kwargs.pop("options", None)

        if model_class or field_title:
            relationship_options = cls._build_relationship_options(
                model_class, field_title
            )
            if options is None:
                options = {}
            options.update(relationship_options)

        return FieldView(
            name=name,
            title=title,
            field_type=field_type,
            options=options,
            model_class=model_class,
            **kwargs,
        )

    @classmethod
    def foreignkey_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        return cls._relationship_field(name, title, "foreignkey", **kwargs)

    @classmethod
    def many_to_many_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        return cls._relationship_field(name, title, "many_to_many", **kwargs)

    @classmethod
    def onetoone_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        return cls._relationship_field(name, title, "OneToOneField", **kwargs)

    @classmethod
    def file_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a file upload field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name, title=title, field_type="file", validators=validation, **kwargs
        )

    @classmethod
    def image_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create an image upload field."""
        # Get existing widget_config from kwargs or create new one
        existing_config = kwargs.pop("widget_config", None)
        if existing_config:
            # Merge with existing config
            existing_config.accept = "image/*"
            widget_config = existing_config
        else:
            # Create new config with image accept
            widget_config = WidgetConfig(accept="image/*")

        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="image",
            widget_config=widget_config,
            validators=validation,
            **kwargs,
        )

    @classmethod
    def json_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a JSON field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name, title=title, field_type="json", validators=validation, **kwargs
        )

    @classmethod
    def color_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a color picker field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name, title=title, field_type="color", validators=validation, **kwargs
        )

    @classmethod
    def primarykey_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a primary key field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="primarykey",
            validators=validation,
            is_primary_key=True,
            **kwargs,
        )

    @classmethod
    def select_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a select field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="choice",
            widget="select",
            validators=validation,
            **kwargs,
        )

    @classmethod
    def radio_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a radio field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="choice",
            widget="radio",
            validators=validation,
            **kwargs,
        )

    @classmethod
    def checkbox_group_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a checkbox group field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="multichoice",
            widget="multiSelect",
            validators=validation,
            **kwargs,
        )

    @classmethod
    def autocomplete_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create an autocomplete field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="string",
            widget="autoComplete",
            validators=validation,
            **kwargs,
        )

    @classmethod
    def toggle_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a toggle field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="boolean",
            widget="switch",
            validators=validation,
            **kwargs,
        )

    @classmethod
    def chips_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a chips field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="multichoice",
            widget="chips",
            validators=validation,
            **kwargs,
        )

    @classmethod
    def listbox_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a listbox field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="multichoice",
            widget="listBox",
            validators=validation,
            **kwargs,
        )

    @classmethod
    def selectbutton_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a select button field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="choice",
            widget="dropdown",
            validators=validation,
            **kwargs,
        )

    @classmethod
    def code_editor_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a code editor field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="json",
            widget="editor",
            validators=validation,
            **kwargs,
        )

    @classmethod
    def color_picker_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a color picker field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="color",
            widget="colorPicker",
            validators=validation,
            **kwargs,
        )

    @classmethod
    def richtext_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a rich text editor field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="string",
            widget="textarea",
            validators=validation,
            **kwargs,
        )

    @classmethod
    def markdown_field(cls, name: str, title: str, **kwargs: Any) -> FieldView:
        """Create a markdown editor field."""
        validation = cls.get_validator(**kwargs)
        return FieldView(
            name=name,
            title=title,
            field_type="string",
            widget="textarea",
            validators=validation,
            **kwargs,
        )
