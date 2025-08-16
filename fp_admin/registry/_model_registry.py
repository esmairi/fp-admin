from typing import Any, Optional, Type

from sqlmodel import SQLModel

from fp_admin.admin.models.helpers import get_model_relationship_fields
from fp_admin.exceptions import ModelError

from ._base import BaseRegistry
from .admin_model_config import AdminModelConfig


class AdminModelRegistry(BaseRegistry[AdminModelConfig]):

    def register(self, config: "AdminModel") -> None:
        module_name = config.model.__module__
        if "." in module_name:
            app_name = module_name.split(".")[-2]
        else:
            app_name = module_name
        columns = (
            config.model.__table__.columns.items()
            if hasattr(config.model, "__table__")
            else []
        )
        primary_keys = [name for name, col in columns if col.primary_key]
        self._registry[config.model.__name__.lower()] = AdminModelConfig(
            model_class=config.model,
            name=config.model.__name__.lower(),
            label=config.label,
            app=app_name,
            relationship_fields=get_model_relationship_fields(config.model),
            direct_fields=list(config.model.model_fields.keys()),
            display_field=config.display_field,
            primary_keys=primary_keys,
        )

    def get_by_model_class(self, model_class: Type[SQLModel]) -> AdminModelConfig:
        models = [
            model
            for model in self._registry.values()
            if model.model_class == model_class
        ]
        if models:
            return models[0]
        raise ModelError(f"Model [{model_class}] not found in registry")


model_registry = AdminModelRegistry()


class AdminModel:
    model: Type[SQLModel]
    label: str
    display_field: Optional[str] = None

    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)

        if hasattr(cls, "model"):
            model_registry.register(cls())
