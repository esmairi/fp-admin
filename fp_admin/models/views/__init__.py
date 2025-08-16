"""
Admin views module for fp-admin.

This module provides the view system for the admin interface, including
view factories, builders, registry, and field specifications.
"""

from .base import (
    BaseView,
    BaseViewFactory,
    FormView,
    FormViewFactory,
    ListView,
    ListViewFactory,
)

__all__ = [
    # Base classes
    "BaseView",
    "BaseViewFactory",
    # View types
    "FormView",
    "ListView",
    # Factories
    "FormViewFactory",
    "ListViewFactory",
]
