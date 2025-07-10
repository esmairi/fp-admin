"""
Blog application views.

This module defines all blog-related views with comprehensive field types
to demonstrate all available fp-admin field capabilities.
"""

from fp_admin.admin.fields import FieldFactory
from fp_admin.admin.views import BaseViewBuilder
from fp_admin.apps.auth.models import User

from .models import (
    Analytics,
    Category,
    Comment,
    Newsletter,
    Post,
    PostTagLink,
    Tag,
)


# Category Views
class CategoryFormView(BaseViewBuilder):
    model = Category
    view_type = "form"
    name = "CategoryForm"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("name", "Name", required=True, max_length=100),
        FieldFactory.string_field("slug", "Slug", required=True, max_length=100),
        FieldFactory.textarea_field("description", "Description", max_length=500),
        FieldFactory.color_field("color", "Color", max_length=7),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.datetime_field("created_at", "Created At"),
        FieldFactory.datetime_field("updated_at", "Updated At"),
    ]

    creation_fields = ["name", "slug", "description", "color", "is_active"]
    allowed_update_fields = ["name", "slug", "description", "color", "is_active"]


class CategoryListView(BaseViewBuilder):
    model = Category
    view_type = "list"
    name = "CategoryList"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("name", "Name"),
        FieldFactory.string_field("slug", "Slug"),
        FieldFactory.color_field("color", "Color"),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.datetime_field("created_at", "Created At"),
    ]


# Tag Views
class TagFormView(BaseViewBuilder):
    model = Tag
    view_type = "form"
    name = "TagForm"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("name", "Name", required=True, max_length=50),
        FieldFactory.string_field("slug", "Slug", required=True, max_length=50),
        FieldFactory.textarea_field("description", "Description", max_length=200),
        FieldFactory.number_field("usage_count", "Usage Count", min_value=0),
        FieldFactory.datetime_field("created_at", "Created At"),
    ]

    creation_fields = ["name", "slug", "description", "usage_count"]
    allowed_update_fields = ["name", "slug", "description", "usage_count"]


class TagListView(BaseViewBuilder):
    model = Tag
    view_type = "list"
    name = "TagList"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("name", "Name"),
        FieldFactory.string_field("slug", "Slug"),
        FieldFactory.number_field("usage_count", "Usage Count"),
        FieldFactory.datetime_field("created_at", "Created At"),
    ]


# Post Views
class PostFormView(BaseViewBuilder):
    model = Post
    view_type = "form"
    name = "PostForm"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("title", "Title", required=True, max_length=200),
        FieldFactory.string_field("slug", "Slug", required=True, max_length=200),
        FieldFactory.textarea_field("excerpt", "Excerpt", max_length=500),
        FieldFactory.textarea_field("content", "Content", required=True),
        FieldFactory.textarea_field(
            "meta_description", "Meta Description", max_length=160
        ),
        FieldFactory.number_field("view_count", "View Count", min_value=0),
        FieldFactory.number_field("like_count", "Like Count", min_value=0),
        FieldFactory.number_field("comment_count", "Comment Count", min_value=0),
        FieldFactory.float_field(
            "reading_time", "Reading Time (minutes)", min_value=0.0
        ),
        FieldFactory.number_field("rating", "Rating", min_value=0.0, max_value=5.0),
        FieldFactory.boolean_field("is_featured", "Featured"),
        FieldFactory.switch_field("is_published", "Published"),
        FieldFactory.switch_field("allow_comments", "Allow Comments"),
        FieldFactory.boolean_field("is_premium", "Premium Content"),
        FieldFactory.datetime_field("created_at", "Created At"),
        FieldFactory.datetime_field("updated_at", "Updated At"),
        FieldFactory.datetime_field("published_at", "Published At"),
        FieldFactory.datetime_field("scheduled_at", "Scheduled At"),
        FieldFactory.choice_field(
            "status",
            "Status",
            options={
                "choices": [
                    {"value": "draft", "label": "Draft"},
                    {"value": "published", "label": "Published"},
                    {"value": "archived", "label": "Archived"},
                ]
            },
        ),
        FieldFactory.file_field("featured_image", "Featured Image"),
        FieldFactory.file_field("attachments", "Attachments"),
        FieldFactory.json_field("seo_data", "SEO Data"),
        FieldFactory.json_field("custom_fields", "Custom Fields"),
        FieldFactory.foreignkey_field(
            "author_id", "Author", model_class=User, field_title="username"
        ),
        FieldFactory.foreignkey_field(
            "category_id", "Category", model_class=Category, field_title="name"
        ),
        FieldFactory.many_to_many_field(
            "tags", "Tags", model_class=Tag, field_title="name"
        ),
    ]

    creation_fields = [
        "title",
        "slug",
        "excerpt",
        "content",
        "meta_description",
        "view_count",
        "like_count",
        "comment_count",
        "reading_time",
        "rating",
        "is_featured",
        "is_published",
        "allow_comments",
        "is_premium",
        "status",
        "featured_image",
        "attachments",
        "seo_data",
        "custom_fields",
        "author_id",
        "category_id",
        "tags",
    ]
    allowed_update_fields = [
        "title",
        "slug",
        "excerpt",
        "content",
        "meta_description",
        "view_count",
        "like_count",
        "comment_count",
        "reading_time",
        "rating",
        "is_featured",
        "is_published",
        "allow_comments",
        "is_premium",
        "status",
        "featured_image",
        "attachments",
        "seo_data",
        "custom_fields",
        "author_id",
        "category_id",
        "tags",
    ]


class PostListView(BaseViewBuilder):
    model = Post
    view_type = "list"
    name = "PostList"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("title", "Title"),
        FieldFactory.string_field("slug", "Slug"),
        FieldFactory.number_field("view_count", "Views"),
        FieldFactory.number_field("like_count", "Likes"),
        FieldFactory.number_field("comment_count", "Comments"),
        FieldFactory.float_field("rating", "Rating"),
        FieldFactory.boolean_field("is_featured", "Featured"),
        FieldFactory.boolean_field("is_published", "Published"),
        FieldFactory.boolean_field("is_premium", "Premium"),
        FieldFactory.choice_field("status", "Status"),
        FieldFactory.datetime_field("created_at", "Created At"),
        FieldFactory.datetime_field("published_at", "Published At"),
        FieldFactory.foreignkey_field(
            "author_id", "Author", model_class=User, field_title="username"
        ),
        FieldFactory.foreignkey_field(
            "category_id", "Category", model_class=Category, field_title="name"
        ),
    ]


# Comment Views
class CommentFormView(BaseViewBuilder):
    model = Comment
    view_type = "form"
    name = "CommentForm"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.textarea_field("content", "Content", required=True),
        FieldFactory.string_field(
            "author_name", "Author Name", required=True, max_length=100
        ),
        FieldFactory.string_field(
            "author_email", "Author Email", required=True, max_length=255
        ),
        FieldFactory.string_field("author_website", "Author Website", max_length=255),
        FieldFactory.float_field("rating", "Rating", min_value=1.0, max_value=5.0),
        FieldFactory.boolean_field("is_approved", "Approved"),
        FieldFactory.switch_field("is_spam", "Spam"),
        FieldFactory.datetime_field("created_at", "Created At"),
        FieldFactory.datetime_field("updated_at", "Updated At"),
        FieldFactory.foreignkey_field(
            "post_id", "Post", model_class=Post, field_title="title", required=True
        ),
        FieldFactory.foreignkey_field(
            "parent_id", "Parent Comment", model_class=Comment, field_title="content"
        ),
        FieldFactory.foreignkey_field(
            "user_id", "User", model_class=User, field_title="username"
        ),
    ]

    creation_fields = [
        "content",
        "author_name",
        "author_email",
        "author_website",
        "rating",
        "is_approved",
        "is_spam",
        "post_id",
        "parent_id",
        "user_id",
    ]
    allowed_update_fields = [
        "content",
        "author_name",
        "author_email",
        "author_website",
        "rating",
        "is_approved",
        "is_spam",
        "post_id",
        "parent_id",
        "user_id",
    ]


class CommentListView(BaseViewBuilder):
    model = Comment
    view_type = "list"
    name = "CommentList"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("author_name", "Author"),
        FieldFactory.string_field("author_email", "Email"),
        FieldFactory.float_field("rating", "Rating"),
        FieldFactory.boolean_field("is_approved", "Approved"),
        FieldFactory.boolean_field("is_spam", "Spam"),
        FieldFactory.datetime_field("created_at", "Created At"),
        FieldFactory.foreignkey_field(
            "post_id", "Post", model_class=Post, field_title="title"
        ),
        FieldFactory.foreignkey_field(
            "user_id", "User", model_class=User, field_title="username"
        ),
    ]


# Newsletter Views
class NewsletterFormView(BaseViewBuilder):
    model = Newsletter
    view_type = "form"
    name = "NewsletterForm"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("email", "Email", required=True, max_length=255),
        FieldFactory.string_field("first_name", "First Name", max_length=100),
        FieldFactory.string_field("last_name", "Last Name", max_length=100),
        FieldFactory.switch_field("is_active", "Active"),
        FieldFactory.switch_field("is_verified", "Verified"),
        FieldFactory.datetime_field("subscribed_at", "Subscribed At"),
        FieldFactory.datetime_field("verified_at", "Verified At"),
        FieldFactory.json_field("preferences", "Preferences"),
    ]

    creation_fields = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_verified",
        "preferences",
    ]
    allowed_update_fields = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_verified",
        "preferences",
    ]


class NewsletterListView(BaseViewBuilder):
    model = Newsletter
    view_type = "list"
    name = "NewsletterList"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("email", "Email"),
        FieldFactory.string_field("first_name", "First Name"),
        FieldFactory.string_field("last_name", "Last Name"),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_verified", "Verified"),
        FieldFactory.datetime_field("subscribed_at", "Subscribed At"),
    ]


# PostTagLink Views (Many-to-Many Link Model)
class PostTagLinkFormView(BaseViewBuilder):
    model = PostTagLink
    view_type = "form"
    name = "PostTagLinkForm"
    fields = [
        FieldFactory.primarykey_field("post_id", "Post ID"),
        FieldFactory.primarykey_field("tag_id", "Tag ID"),
        FieldFactory.foreignkey_field(
            "post_id", "Post", model_class=Post, field_title="title", required=True
        ),
        FieldFactory.foreignkey_field(
            "tag_id", "Tag", model_class=Tag, field_title="name", required=True
        ),
    ]

    creation_fields = ["post_id", "tag_id"]
    allowed_update_fields = ["post_id", "tag_id"]


class PostTagLinkListView(BaseViewBuilder):
    model = PostTagLink
    view_type = "list"
    name = "PostTagLinkList"
    fields = [
        FieldFactory.primarykey_field("post_id", "Post ID"),
        FieldFactory.primarykey_field("tag_id", "Tag ID"),
        FieldFactory.foreignkey_field(
            "post_id", "Post", model_class=Post, field_title="title"
        ),
        FieldFactory.foreignkey_field(
            "tag_id", "Tag", model_class=Tag, field_title="name"
        ),
    ]


# Analytics Views
class AnalyticsFormView(BaseViewBuilder):
    model = Analytics
    view_type = "form"
    name = "AnalyticsForm"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field(
            "page_url", "Page URL", required=True, max_length=500
        ),
        FieldFactory.textarea_field("user_agent", "User Agent", max_length=500),
        FieldFactory.string_field("ip_address", "IP Address", max_length=45),
        FieldFactory.string_field("referrer", "Referrer", max_length=500),
        FieldFactory.float_field(
            "session_duration", "Session Duration (seconds)", min_value=0.0
        ),
        FieldFactory.number_field(
            "scroll_depth", "Scroll Depth (%)", min_value=0.0, max_value=100.0
        ),
        FieldFactory.boolean_field("is_bounce", "Bounce Visit"),
        FieldFactory.datetime_field("visited_at", "Visited At"),
        FieldFactory.foreignkey_field(
            "post_id", "Post", model_class=Post, field_title="title"
        ),
        FieldFactory.foreignkey_field(
            "user_id", "User", model_class=User, field_title="username"
        ),
    ]

    creation_fields = [
        "page_url",
        "user_agent",
        "ip_address",
        "referrer",
        "session_duration",
        "scroll_depth",
        "is_bounce",
        "visited_at",
        "post_id",
        "user_id",
    ]
    allowed_update_fields = [
        "page_url",
        "user_agent",
        "ip_address",
        "referrer",
        "session_duration",
        "scroll_depth",
        "is_bounce",
        "visited_at",
        "post_id",
        "user_id",
    ]


class AnalyticsListView(BaseViewBuilder):
    model = Analytics
    view_type = "list"
    name = "AnalyticsList"
    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("page_url", "Page URL"),
        FieldFactory.string_field("ip_address", "IP Address"),
        FieldFactory.float_field("session_duration", "Session Duration"),
        FieldFactory.number_field("scroll_depth", "Scroll Depth"),
        FieldFactory.boolean_field("is_bounce", "Bounce"),
        FieldFactory.datetime_field("visited_at", "Visited At"),
        FieldFactory.foreignkey_field(
            "post_id", "Post", model_class=Post, field_title="title"
        ),
        FieldFactory.foreignkey_field(
            "user_id", "User", model_class=User, field_title="username"
        ),
    ]
