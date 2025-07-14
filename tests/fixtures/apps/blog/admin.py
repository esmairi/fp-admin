"""
Blog application admin configuration.

This module configures the admin interface for all blog models,
following the simple pattern from the auth app.
"""

from fp_admin.admin.models import AdminModel

from .models import Analytics, Category, Comment, Newsletter, Post, PostTagLink, Tag


class CategoryAdmin(AdminModel):
    model = Category
    label = "Categories"


class TagAdmin(AdminModel):
    model = Tag
    label = "Tags"


class PostAdmin(AdminModel):
    model = Post
    label = "Posts"


class CommentAdmin(AdminModel):
    model = Comment
    label = "Comments"


class NewsletterAdmin(AdminModel):
    model = Newsletter
    label = "Newsletter Subscriptions"


class AnalyticsAdmin(AdminModel):
    model = Analytics
    label = "Analytics"


class PostTagLinkAdmin(AdminModel):
    model = PostTagLink
    label = "PostTagLink"
