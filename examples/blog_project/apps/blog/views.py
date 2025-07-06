"""
Blog application views.

This module provides view configurations for the blog models,
following the auth app pattern with simple custom views.
"""

from fp_admin.admin.fields import FieldView
from fp_admin.admin.views import BaseViewBuilder

from .models import BlogSettings, Category, Comment, Post, Tag


class CategoryFormView(BaseViewBuilder):
    model = Category
    view_type = "form"
    name = "CategoryForm"
    fields = [
        FieldView(name="name", label="Name", field_type="text"),
        FieldView(name="slug", label="Slug", field_type="text"),
        FieldView(name="description", label="Description", field_type="textarea"),
        FieldView(name="color", label="Color", field_type="text", widget="color"),
        FieldView(
            name="is_active", label="Is Active", field_type="checkbox", widget="toggle"
        ),
    ]


class CategoryListView(BaseViewBuilder):
    model = Category
    view_type = "list"
    name = "CategoryList"


class TagFormView(BaseViewBuilder):
    model = Tag
    view_type = "form"
    name = "TagForm"
    fields = [
        FieldView(name="name", label="Name", field_type="text"),
        FieldView(name="slug", label="Slug", field_type="text"),
        FieldView(name="description", label="Description", field_type="text"),
    ]


class TagListView(BaseViewBuilder):
    model = Tag
    view_type = "list"
    name = "TagList"


class PostFormView(BaseViewBuilder):
    model = Post
    view_type = "form"
    name = "PostForm"
    fields = [
        FieldView(name="title", label="Title", field_type="text"),
        FieldView(name="slug", label="Slug", field_type="text"),
        FieldView(
            name="content", label="Content", field_type="textarea", widget="richtext"
        ),
        FieldView(name="excerpt", label="Excerpt", field_type="textarea"),
        FieldView(name="featured_image", label="Featured Image", field_type="file"),
        FieldView(
            name="status",
            label="Status",
            field_type="select",
            widget="radio",
            options=[
                {"title": "Draft", "value": "draft"},
                {"title": "Published", "value": "published"},
                {"title": "Archived", "value": "archived"},
            ],
        ),
        FieldView(
            name="is_featured",
            label="Is Featured",
            field_type="checkbox",
            widget="toggle",
        ),
        FieldView(
            name="allow_comments",
            label="Allow Comments",
            field_type="checkbox",
            widget="switch",
        ),
    ]


class PostListView(BaseViewBuilder):
    model = Post
    view_type = "list"
    name = "PostList"


class CommentFormView(BaseViewBuilder):
    model = Comment
    view_type = "form"
    name = "CommentForm"
    fields = [
        FieldView(name="content", label="Content", field_type="text"),
        FieldView(name="is_approved", label="Is Approved", field_type="text"),
        FieldView(name="is_spam", label="Is Spam", field_type="text"),
    ]


class CommentListView(BaseViewBuilder):
    model = Comment
    view_type = "list"
    name = "CommentList"


class BlogSettingsFormView(BaseViewBuilder):
    model = BlogSettings
    view_type = "form"
    name = "BlogSettingsForm"
    fields = [
        FieldView(name="site_name", label="Site Name", field_type="text"),
        FieldView(
            name="site_description", label="Site Description", field_type="textarea"
        ),
        FieldView(
            name="posts_per_page",
            label="Posts Per Page",
            field_type="number",
            widget="range",
        ),
        FieldView(
            name="allow_registration",
            label="Allow Registration",
            field_type="checkbox",
            widget="toggle",
        ),
        FieldView(
            name="moderate_comments",
            label="Moderate Comments",
            field_type="checkbox",
            widget="switch",
        ),
        FieldView(
            name="auto_approve_comments",
            label="Auto-approve Comments",
            field_type="checkbox",
            widget="switch",
        ),
    ]
