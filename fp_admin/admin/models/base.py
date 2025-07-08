from typing import Any, Dict, List, Optional, Type, cast

from sqlmodel import SQLModel

from fp_admin.exceptions import ModelError


class AdminModelRegistry:
    _registry: List[Dict[str, Any]] = []

    @classmethod
    def register(cls, config: "AdminModel") -> None:
        cls._registry.append(
            {
                "model": config.model,
                "model_name": config.model.__name__.lower(),
                "model_label": config.label,
                "app": config.model.__module__.split(".")[-2],
            }
        )

    @classmethod
    def all(cls) -> List[Dict[str, Any]]:
        return cls._registry

    @classmethod
    def get_model_class(cls, model_name: str) -> Type[SQLModel]:
        models = [
            model for model in cls._registry if model.get("model_name") == model_name
        ]
        if models:
            return cast(Type[SQLModel], models[0]["model"])
        raise ModelError(f"Model [{model_name}] not found in registry")


model_registry = AdminModelRegistry()


class AdminModel:
    model: Type[SQLModel]
    label: Optional[str] = None

    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "model"):
            model_registry.register(cls())
