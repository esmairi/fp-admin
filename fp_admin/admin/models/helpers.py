from typing import List, Type

from sqlalchemy.inspection import inspect
from sqlmodel import SQLModel

from fp_admin.exceptions import ModelError


def get_model_relationship_fields(model_class: Type[SQLModel]) -> List[str]:
    """
    Returns relationship field names from a SQLModel class.

    Raises:
        ModelError: If inspection fails
    """
    mapper = inspect(model_class)
    if not mapper:
        raise ModelError("Failed to inspect model class.")
    return list(mapper.relationships.keys())


def get_pk_names(model_cls: Type[SQLModel]) -> list[str]:
    if not hasattr(model_cls, "__table__"):
        return []
    return [
        name for name, col in model_cls.__table__.columns.items() if col.primary_key
    ]
