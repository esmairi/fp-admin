from itertools import chain
from typing import Dict, List, Type

from sqlmodel import SQLModel

from fp_admin.admin.views.views_types import BaseView


class ViewRegistry:
    _views: Dict[str, List[BaseView]] = {}

    @classmethod
    def register(cls, model: Type[SQLModel], view: BaseView) -> None:
        model_name = model.__name__.lower()
        if model_name not in cls._views:
            cls._views[model_name] = []
        cls._views[model_name].append(view)

    @classmethod
    def all(cls) -> Dict[str, List[BaseView]]:
        return cls._views

    @classmethod
    def get(cls, model_name: str) -> List[BaseView]:
        return cls._views.get(model_name, [])

    @classmethod
    def find_by_name(cls, view_name: str) -> BaseView | None:
        target_view = [
            v for v in chain.from_iterable(cls._views.values()) if v.name == view_name
        ]
        if target_view:
            return target_view[0]
        return None


view_registry = ViewRegistry()
