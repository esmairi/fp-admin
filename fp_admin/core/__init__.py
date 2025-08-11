"""
Core package for fp-admin.

This package contains core functionality including database management,
module loading, and utility functions.
"""

from .db import DatabaseManager, db_manager, get_session
from .loader import (
    get_loaded_apps,
    load_app_routers,
    load_module,
    load_modules,
    reload_app,
)

__all__ = [
    # Database
    "DatabaseManager",
    "db_manager",
    "get_session",
    "load_modules",
    "load_app_routers",
    "get_loaded_apps",
    # Loader
    "load_app_routers",
    "load_module",
    "load_modules",
    "reload_app",
    "get_loaded_apps",
]
