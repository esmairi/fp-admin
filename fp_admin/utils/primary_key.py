from typing import Type, cast

from sqlalchemy.inspection import inspect
from sqlmodel import SQLModel

from fp_admin.exceptions import ModelError


def get_primary_key_field(model_class: Type[SQLModel]) -> str:
    """Get the primary key field name from a model.

    Args:
        model_class: The model class

    Returns:
        The primary key field name

    Raises:
        ModelError: If no primary key is found or multiple primary keys exist
    """
    mapper = inspect(model_class)
    if not mapper:
        raise ModelError("Error: Inspect Model")

    primary_keys = mapper.primary_key
    if not primary_keys or len(primary_keys) == 0:
        raise ModelError(f"No primary key found in model {model_class.__name__}")

    if len(primary_keys) > 1:
        raise ModelError(f"Multiple primary keys found in model {model_class.__name__}")

    return cast(str, primary_keys[0].name)
