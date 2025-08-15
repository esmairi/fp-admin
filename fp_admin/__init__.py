"""
FastAPI Admin Framework

A modern, FastAPI-based admin framework that provides automatic CRUD interfaces
and admin panels for SQLModel-based applications.
"""

from contextlib import asynccontextmanager
from importlib.metadata import version as metadata_version
from typing import Any, AsyncGenerator, Callable, Optional

from fastapi import FastAPI

from fp_admin.constants import APP_NAME
from fp_admin.core import db_manager
from fp_admin.settings_loader import settings

# Version information
__version__ = metadata_version("fp-admin")

LifespanType = Callable[[FastAPI], AsyncGenerator[None, None]]


class FastAPIAdmin(FastAPI):
    """FastAPI Admin application class."""

    def __init__(
        self,
        *args: Any,
        lifespan: Optional[LifespanType] = None,
        disable_db_init: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize the FastAPI Admin application."""

        @asynccontextmanager
        async def combined_lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
            # 🚀 Startup
            if not disable_db_init:
                await db_manager.init_db()
            if lifespan is not None:
                async with lifespan(app):  # type: ignore
                    yield
            else:
                yield

        super().__init__(
            title=APP_NAME,
            version=metadata_version("fp-admin"),
            description="FastAPI Admin Framework",
            *args,
            lifespan=combined_lifespan,
            **kwargs,
        )
        self.__setup()

    def __setup(self) -> None:
        """Set up the admin application."""
        from fp_admin.api import api_router
        from fp_admin.core.loader import load_modules

        # Load all modules (models, views, admin, apps)
        load_modules(self)

        # Include the API router
        self.include_router(api_router)

        self.set_cors()

    def set_cors(self) -> None:
        if settings.CORS_ORIGINS:
            from fastapi.middleware.cors import CORSMiddleware

            self.add_middleware(
                CORSMiddleware,
                allow_origins=settings.CORS_ORIGINS,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )


# Export main components
__all__ = [
    "__version__",
    "settings",
    "FastAPIAdmin",
]
