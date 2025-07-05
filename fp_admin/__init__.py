from typing import Any

from fastapi import FastAPI

from fp_admin.settings_loader import settings


class FpAdmin(FastAPI):
    admin_path: str = "/admin"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__setup()

    def __setup(self) -> None:
        from fp_admin.api import api_router
        from fp_admin.core.loader import load_modules

        load_modules(self)
        self.include_router(api_router, prefix=self.admin_path)


__all__ = ["settings", "FpAdmin"]
