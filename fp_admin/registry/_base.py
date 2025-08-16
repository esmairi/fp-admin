from typing import Dict, Generic, TypeVar

T = TypeVar("T")


class BaseRegistry(Generic[T]):
    def __init__(self) -> None:
        self._registry: Dict[str, T] = {}

    def list(self) -> Dict[str, T]:
        return self._registry

    def get(self, name: str) -> T | None:
        return self._registry.get(name)
