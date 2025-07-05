"""
Blog application admin configuration.

This module configures the admin interface for all blog models,
following the simple pattern from the auth app.
"""

from fp_admin.admin.models import AdminModel

from .models import BlogSettings, Category, Comment, Post, Tag


class CategoryAdmin(AdminModel):
    """Admin configuration for Category model."""

    model = Category
    label = "Categories"


class TagAdmin(AdminModel):
    """Admin configuration for Tag model."""

    model = Tag
    label = "Tags"


class PostAdmin(AdminModel):
    """Admin configuration for Post model."""

    model = Post
    label = "Posts"

    # File upload configuration
    file_upload_fields = {
        "featured_image": {
            "upload_dir": "uploads/posts/images",
            "allowed_extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
            "max_size": 5 * 1024 * 1024,  # 5MB
            "generate_thumbnail": True,
        }
    }


class CommentAdmin(AdminModel):
    """Admin configuration for Comment model."""

    model = Comment
    label = "Comments"


class BlogSettingsAdmin(AdminModel):
    """Admin configuration for BlogSettings model."""

    model = BlogSettings
    label = "Blog Settings"
