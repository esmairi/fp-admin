"""
Blog application models.

This module defines all blog-related models with comprehensive field types
to demonstrate all available fp-admin field capabilities.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel

from fp_admin.apps.auth.models import User


class PostStatus(str, Enum):
    """Post status enumeration."""

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Category(SQLModel, table=True):
    """Blog category model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, description="Category name")
    slug: str = Field(max_length=100, unique=True, description="URL slug")
    description: Optional[str] = Field(
        default=None, max_length=500, description="Category description"
    )
    color: Optional[str] = Field(
        default=None, max_length=7, description="Category color hex code"
    )
    is_active: bool = Field(default=True, description="Whether category is active")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )

    # Relationships
    posts: List["Post"] = Relationship(back_populates="category")


class PostTagLink(SQLModel, table=True):
    """Many-to-many relationship between posts and tags."""

    post_id: int = Field(foreign_key="post.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


class Tag(SQLModel, table=True):
    """Blog tag model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True, description="Tag name")
    slug: str = Field(max_length=50, unique=True, description="URL slug")
    description: Optional[str] = Field(
        default=None, max_length=200, description="Tag description"
    )
    usage_count: int = Field(default=0, description="Number of posts using this tag")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )

    # Relationships
    posts: List["Post"] = Relationship(back_populates="tags", link_model=PostTagLink)


class Post(SQLModel, table=True):
    """Blog post model with all field types."""

    id: Optional[int] = Field(default=None, primary_key=True)

    # String fields
    title: str = Field(max_length=200, description="Post title")
    slug: str = Field(max_length=200, unique=True, description="URL slug")
    excerpt: Optional[str] = Field(
        default=None, max_length=500, description="Post excerpt"
    )
    content: str = Field(description="Post content")
    meta_description: Optional[str] = Field(
        default=None, max_length=160, description="SEO meta description"
    )

    # Number fields
    view_count: int = Field(default=0, description="Number of views")
    like_count: int = Field(default=0, description="Number of likes")
    comment_count: int = Field(default=0, description="Number of comments")
    reading_time: float = Field(
        default=0.0, description="Estimated reading time in minutes"
    )
    rating: float = Field(default=0.0, ge=0.0, le=5.0, description="Average rating")

    # Boolean fields
    is_featured: bool = Field(default=False, description="Whether post is featured")
    is_published: bool = Field(default=False, description="Whether post is published")
    allow_comments: bool = Field(
        default=True, description="Whether comments are allowed"
    )
    is_premium: bool = Field(
        default=False, description="Whether post is premium content"
    )

    # Date/Time fields
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )
    published_at: Optional[datetime] = Field(
        default=None, description="Publication timestamp"
    )
    scheduled_at: Optional[datetime] = Field(
        default=None, description="Scheduled publication time"
    )

    # Choice fields
    status: PostStatus = Field(default=PostStatus.DRAFT, description="Post status")

    # File fields
    featured_image: Optional[str] = Field(
        default=None, description="Featured image path"
    )
    attachments: Optional[str] = Field(
        default=None, description="JSON array of attachment paths"
    )

    # JSON fields
    seo_data: Optional[Dict[str, Any]] = Field(
        default=None, sa_type=JSON, description="SEO metadata"
    )
    custom_fields: Optional[Dict[str, Any]] = Field(
        default=None, sa_type=JSON, description="Custom post fields"
    )

    # Foreign key relationships
    author_id: int = Field(foreign_key="user.id", description="Post author")
    category_id: Optional[int] = Field(
        default=None, foreign_key="category.id", description="Post category"
    )

    # Relationships
    author: User = Relationship(back_populates=None)  # User model can't be modified
    category: Optional[Category] = Relationship(back_populates="posts")
    tags: List[Tag] = Relationship(back_populates="posts", link_model=PostTagLink)
    comments: List["Comment"] = Relationship(back_populates="post")
    analytics: List["Analytics"] = Relationship(back_populates="post")


class Comment(SQLModel, table=True):
    """Blog comment model."""

    id: Optional[int] = Field(default=None, primary_key=True)

    # String fields
    content: str = Field(description="Comment content")
    author_name: str = Field(max_length=100, description="Commenter name")
    author_email: str = Field(max_length=255, description="Commenter email")
    author_website: Optional[str] = Field(
        default=None, max_length=255, description="Commenter website"
    )

    # Number fields
    rating: Optional[float] = Field(
        default=None, ge=1.0, le=5.0, description="Comment rating"
    )

    # Boolean fields
    is_approved: bool = Field(default=False, description="Whether comment is approved")
    is_spam: bool = Field(default=False, description="Whether comment is spam")

    # Date/Time fields
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )

    # Foreign key relationships
    post_id: int = Field(foreign_key="post.id", description="Commented post")
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", description="Commenter user"
    )

    # Relationships
    post: Post = Relationship(back_populates="comments")
    user: Optional[User] = Relationship(back_populates=None)

    parent_id: Optional[int] = Field(default=None, foreign_key="comment.id")

    # Self-referential relationship
    parent: Optional["Comment"] = Relationship(
        back_populates="replies",
        sa_relationship_kwargs={
            "remote_side": "Comment.id",
        },
    )
    replies: List["Comment"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={"foreign_keys": "[Comment.parent_id]"},
    )


class Newsletter(SQLModel, table=True):
    """Newsletter subscription model."""

    id: Optional[int] = Field(default=None, primary_key=True)

    # String fields
    email: str = Field(max_length=255, unique=True, description="Subscriber email")
    first_name: Optional[str] = Field(
        default=None, max_length=100, description="Subscriber first name"
    )
    last_name: Optional[str] = Field(
        default=None, max_length=100, description="Subscriber last name"
    )

    # Boolean fields
    is_active: bool = Field(default=True, description="Whether subscription is active")
    is_verified: bool = Field(default=False, description="Whether email is verified")

    # Date/Time fields
    subscribed_at: datetime = Field(
        default_factory=datetime.now, description="Subscription timestamp"
    )
    verified_at: Optional[datetime] = Field(
        default=None, description="Email verification timestamp"
    )

    # JSON fields
    preferences: Optional[Dict[str, Any]] = Field(
        default=None, sa_type=JSON, description="Subscriber preferences"
    )


class Analytics(SQLModel, table=True):
    """Blog analytics model."""

    id: Optional[int] = Field(default=None, primary_key=True)

    # String fields
    page_url: str = Field(max_length=500, description="Page URL")
    user_agent: Optional[str] = Field(
        default=None, max_length=500, description="User agent string"
    )
    ip_address: Optional[str] = Field(
        default=None, max_length=45, description="Visitor IP address"
    )
    referrer: Optional[str] = Field(
        default=None, max_length=500, description="Referrer URL"
    )

    # Number fields
    session_duration: float = Field(
        default=0.0, description="Session duration in seconds"
    )
    scroll_depth: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Scroll depth percentage"
    )

    # Boolean fields
    is_bounce: bool = Field(default=True, description="Whether this is a bounce visit")

    # Date/Time fields
    visited_at: datetime = Field(
        default_factory=datetime.now, description="Visit timestamp"
    )

    # Foreign key relationships
    post_id: Optional[int] = Field(
        default=None, foreign_key="post.id", description="Visited post"
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", description="Visitor user"
    )

    # Relationships
    post: Optional[Post] = Relationship(back_populates="analytics")
    user: Optional[User] = Relationship(back_populates=None)


[
    model.model_rebuild()
    for model in [Analytics, Newsletter, Comment, Post, Tag, PostTagLink, Category]
]
