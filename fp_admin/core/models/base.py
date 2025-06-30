from typing import List, Type, Optional
from sqlmodel import SQLModel


class AdminModelRegistry:
    _registry: List[dict] = []

    @classmethod
    def register(cls, config: "AdminModel"):
        cls._registry.append(
            {
                "model": config.model,
                "model_name": config.model.__name__,
                "model_label": config.label,
                "apps": config.model.__module__.split(".")[-2],
            }
        )

    @classmethod
    def all(cls):
        return cls._registry


admin_model_registry = AdminModelRegistry()


class AdminModel:
    model: Type[SQLModel]
    label: Optional[str] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "model"):
            admin_model_registry.register(cls())
