"""
Blog application configuration.

This module configures the blog application following the auth app pattern.
"""

from fp_admin.admin.apps import AppConfig


class BlogConfig(AppConfig):
    """Blog application configuration."""

    name = "blog"
    verbose_name = "Blog"
