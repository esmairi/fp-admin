"""
Blog application views.

This module defines all blog-related views with comprehensive field types
to demonstrate all available fp-admin field capabilities.
"""

from fp_admin.apps.auth.models import User
from fp_admin.models.field import FieldFactory
from fp_admin.registry import ViewBuilder

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
class CategoryFormView(ViewBuilder):
    model = Category
    view_type = "form"
    name = "CategoryForm"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field("name", title="Name", required=True, max_length=100),
        FieldFactory.string_field("slug", title="Slug", required=True, max_length=100),
        FieldFactory.text_field("description", title="Description", max_length=500),
        FieldFactory.boolean_field("is_active", title="Active"),
        FieldFactory.datetime_field("created_at", title="Created At"),
        FieldFactory.datetime_field("updated_at", title="Updated At"),
    ]

    creation_fields = ["name", "slug", "description", "is_active"]
    allowed_update_fields = ["name", "slug", "description", "is_active"]


class CategoryListView(ViewBuilder):
    model = Category
    view_type = "list"
    name = "CategoryList"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field("name", title="Name"),
        FieldFactory.string_field("slug", title="Slug"),
        FieldFactory.boolean_field("is_active", title="Active"),
        FieldFactory.datetime_field("created_at", title="Created At"),
    ]


# Tag Views
class TagFormView(ViewBuilder):
    model = Tag
    view_type = "form"
    name = "TagForm"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field("name", title="Name", required=True, max_length=50),
        FieldFactory.string_field("slug", title="Slug", required=True, max_length=50),
        FieldFactory.text_field("description", title="Description", max_length=200),
        FieldFactory.number_field("usage_count", title="Usage Count", gt=0),
        FieldFactory.datetime_field("created_at", title="Created At"),
    ]

    creation_fields = ["name", "slug", "description", "usage_count"]
    allowed_update_fields = ["name", "slug", "description", "usage_count"]


class TagListView(ViewBuilder):
    model = Tag
    view_type = "list"
    name = "TagList"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field("name", title="Name"),
        FieldFactory.string_field("slug", title="Slug"),
        FieldFactory.number_field("usage_count", title="Usage Count"),
        FieldFactory.datetime_field("created_at", title="Created At"),
    ]


# Post Views
class PostFormView(ViewBuilder):
    model = Post
    view_type = "form"
    name = "PostForm"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field(
            "title", title="Title", required=True, max_length=200
        ),
        FieldFactory.string_field("slug", title="Slug", required=True, max_length=200),
        FieldFactory.text_field("excerpt", title="Excerpt", max_length=500),
        FieldFactory.text_field("content", title="Content", required=True),
        FieldFactory.text_field(
            "meta_description", title="Meta Description", max_length=160
        ),
        FieldFactory.number_field("view_count", title="View Count", ge=0),
        FieldFactory.number_field("like_count", title="Like Count", ge=0),
        FieldFactory.number_field("comment_count", title="Comment Count", ge=0),
        FieldFactory.float_field(
            "reading_time", title="Reading Time (minutes)", ge=0.0
        ),
        FieldFactory.float_field("rating", title="Rating", ge=0.0, le=5.0),
        FieldFactory.boolean_field("is_featured", title="Featured"),
        FieldFactory.boolean_field("is_published", title="Is Published"),
        FieldFactory.boolean_field("is_premium", title="Premium Content"),
        FieldFactory.boolean_field("allow_comments", title="Allow comments"),
        FieldFactory.datetime_field("created_at", title="Created At"),
        FieldFactory.datetime_field("updated_at", title="Updated At"),
        FieldFactory.datetime_field("published_at", title="Published At"),
        FieldFactory.datetime_field("scheduled_at", title="Scheduled At"),
        FieldFactory.choice_field(
            "status",
            title="Status",
            options={
                "choices": [
                    {"value": "draft", "label": "Draft"},
                    {"value": "published", "label": "Published"},
                    {"value": "archived", "label": "Archived"},
                ]
            },
        ),
        FieldFactory.file_field("featured_image", title="Featured Image"),
        FieldFactory.file_field("attachments", title="Attachments"),
        FieldFactory.json_field("seo_data", title="SEO Data"),
        FieldFactory.json_field("custom_fields", title="Custom Fields"),
        FieldFactory.foreignkey_field(
            "author_id", title="Author", model_class=User, display_field="username"
        ),
        FieldFactory.foreignkey_field(
            "category_id", title="Category", model_class=Category, display_field="name"
        ),
        FieldFactory.many_to_many_field(
            "tags", title="Tags", model_class=Tag, display_field="name"
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


class PostListView(ViewBuilder):
    model = Post
    view_type = "list"
    name = "PostList"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field("title", title="Title"),
        FieldFactory.string_field("slug", title="Slug"),
        FieldFactory.number_field("view_count", title="Views"),
        FieldFactory.number_field("like_count", title="Likes"),
        FieldFactory.number_field("comment_count", title="Comments"),
        FieldFactory.float_field("rating", title="Rating"),
        FieldFactory.boolean_field("is_featured", title="Featured"),
        FieldFactory.boolean_field("is_published", title="Published"),
        FieldFactory.boolean_field("is_premium", title="Premium"),
        FieldFactory.choice_field("status", title="Status"),
        FieldFactory.datetime_field("created_at", title="Created At"),
        FieldFactory.datetime_field("published_at", title="Published At"),
        FieldFactory.foreignkey_field(
            "author_id", title="Author", model_class=User, display_field="username"
        ),
        FieldFactory.foreignkey_field(
            "category_id", title="Category", model_class=Category, display_field="name"
        ),
    ]


# Comment Views
class CommentFormView(ViewBuilder):
    model = Comment
    view_type = "form"
    name = "CommentForm"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.text_field("content", title="Content", required=True),
        FieldFactory.string_field(
            "author_name", title="Author Name", required=True, max_length=100
        ),
        FieldFactory.string_field(
            "author_email", title="Author Email", required=True, max_length=255
        ),
        FieldFactory.string_field(
            "author_website", title="Author Website", max_length=255
        ),
        FieldFactory.float_field("rating", title="Rating", ge=1.0, le=5.0),
        FieldFactory.boolean_field("is_approved", title="Approved"),
        FieldFactory.datetime_field("created_at", title="Created At"),
        FieldFactory.datetime_field("updated_at", title="Updated At"),
        FieldFactory.foreignkey_field(
            "post_id",
            title="Post",
            model_class=Post,
            display_field="title",
            required=True,
        ),
        FieldFactory.foreignkey_field(
            "parent_id",
            title="Parent Comment",
            model_class=Comment,
            display_field="content",
        ),
        FieldFactory.foreignkey_field(
            "user_id", title="User", model_class=User, display_field="username"
        ),
    ]

    creation_fields = [
        "content",
        "author_name",
        "author_email",
        "author_website",
        "rating",
        "is_approved",
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
        "post_id",
        "parent_id",
        "user_id",
    ]


class CommentListView(ViewBuilder):
    model = Comment
    view_type = "list"
    name = "CommentList"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field("author_name", title="Author"),
        FieldFactory.string_field("author_email", title="Email"),
        FieldFactory.float_field("rating", title="Rating"),
        FieldFactory.boolean_field("is_approved", title="Approved"),
        FieldFactory.boolean_field("is_spam", title="Spam"),
        FieldFactory.datetime_field("created_at", title="Created At"),
        FieldFactory.foreignkey_field(
            "post_id", title="Post", model_class=Post, display_field="title"
        ),
        FieldFactory.foreignkey_field(
            "user_id", title="User", model_class=User, display_field="username"
        ),
    ]


# Newsletter Views
class NewsletterFormView(ViewBuilder):
    model = Newsletter
    view_type = "form"
    name = "NewsletterForm"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field(
            "email", title="Email", required=True, max_length=255
        ),
        FieldFactory.string_field("first_name", title="First Name", max_length=100),
        FieldFactory.string_field("last_name", title="Last Name", max_length=100),
        FieldFactory.datetime_field("subscribed_at", title="Subscribed At"),
        FieldFactory.datetime_field("verified_at", title="Verified At"),
        FieldFactory.boolean_field("is_active", title="is Active"),
        FieldFactory.boolean_field("is_verified", title="is Verified"),
        FieldFactory.json_field("preferences", title="Preferences"),
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


class NewsletterListView(ViewBuilder):
    model = Newsletter
    view_type = "list"
    name = "NewsletterList"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field("email", title="Email"),
        FieldFactory.string_field("first_name", title="First Name"),
        FieldFactory.string_field("last_name", title="Last Name"),
        FieldFactory.boolean_field("is_active", title="Active"),
        FieldFactory.boolean_field("is_verified", title="Verified"),
        FieldFactory.datetime_field("subscribed_at", title="Subscribed At"),
    ]


# PostTagLink Views (Many-to-Many Link Model)
class PostTagLinkFormView(ViewBuilder):
    model = PostTagLink
    view_type = "form"
    name = "PostTagLinkForm"
    fields = [
        FieldFactory.primary_key_field("post_id", title="Post ID"),
        FieldFactory.primary_key_field("tag_id", title="Tag ID"),
        FieldFactory.foreignkey_field(
            "post_id",
            title="Post",
            model_class=Post,
            display_field="title",
            required=True,
        ),
        FieldFactory.foreignkey_field(
            "tag_id", title="Tag", model_class=Tag, display_field="name", required=True
        ),
    ]

    creation_fields = ["post_id", "tag_id"]
    allowed_update_fields = ["post_id", "tag_id"]


class PostTagLinkListView(ViewBuilder):
    model = PostTagLink
    view_type = "list"
    name = "PostTagLinkList"
    fields = [
        FieldFactory.primary_key_field("post_id", title="Post ID"),
        FieldFactory.primary_key_field("tag_id", title="Tag ID"),
        FieldFactory.foreignkey_field(
            "post_id", title="Post", model_class=Post, display_field="title"
        ),
        FieldFactory.foreignkey_field(
            "tag_id", title="Tag", model_class=Tag, display_field="name"
        ),
    ]


# Analytics Views
class AnalyticsFormView(ViewBuilder):
    model = Analytics
    view_type = "form"
    name = "AnalyticsForm"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field(
            "page_url", title="Page URL", required=True, max_length=500
        ),
        FieldFactory.text_field("user_agent", title="User Agent", max_length=500),
        FieldFactory.string_field("ip_address", title="IP Address", max_length=45),
        FieldFactory.string_field("referrer", title="Referrer", max_length=500),
        FieldFactory.float_field(
            "session_duration", title="Session Duration (seconds)", ge=0.0
        ),
        FieldFactory.number_field(
            "scroll_depth", title="Scroll Depth (%)", ge=0.0, le=100.0
        ),
        FieldFactory.boolean_field("is_bounce", title="Bounce Visit"),
        FieldFactory.datetime_field("visited_at", title="Visited At"),
        FieldFactory.foreignkey_field(
            "post_id", title="Post", model_class=Post, display_field="title"
        ),
        FieldFactory.foreignkey_field(
            "user_id", title="User", model_class=User, display_field="username"
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


class AnalyticsListView(ViewBuilder):
    model = Analytics
    view_type = "list"
    name = "AnalyticsList"
    fields = [
        FieldFactory.primary_key_field("id", title="ID"),
        FieldFactory.string_field("page_url", title="Page URL"),
        FieldFactory.string_field("ip_address", title="IP Address"),
        FieldFactory.float_field("session_duration", title="Session Duration"),
        FieldFactory.number_field("scroll_depth", title="Scroll Depth"),
        FieldFactory.boolean_field("is_bounce", title="Bounce"),
        FieldFactory.datetime_field("visited_at", title="Visited At"),
        FieldFactory.foreignkey_field(
            "post_id", title="Post", model_class=Post, display_field="title"
        ),
        FieldFactory.foreignkey_field(
            "user_id", title="User", model_class=User, display_field="username"
        ),
    ]
