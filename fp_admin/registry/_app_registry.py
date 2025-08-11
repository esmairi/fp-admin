from ._base import BaseRegistry


class AppRegistry(BaseRegistry["AppConfig"]):
    """Registry for apps"""

    def register(self, config: "AppConfig") -> None:
        self._registry[config.name] = config


apps_registry = AppRegistry()


class AppConfig:
    name: str
    verbose_name: str

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if not hasattr(cls, "name"):
            raise ValueError(f"{cls.__name__} must define a `name`")
        apps_registry.register(cls())
