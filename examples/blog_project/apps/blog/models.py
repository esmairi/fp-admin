"""
Blog application models.

This module contains all the models for the blog application including
Category, Post, Comment, and Tag models with proper relationships.
Uses the User model from fp_admin.apps.auth.models.
"""

from datetime import UTC, datetime
from typing import List, Literal, Optional

from sqlmodel import Field, Relationship, SQLModel

# Import User from auth app
from fp_admin.apps.auth.models import User


class BlogUser(User, table=False):
    posts: List["Post"] = Relationship(back_populates="author")
    comments: List["Comment"] = Relationship(back_populates="author")


class Category(SQLModel, table=True):
    """Category model for organizing blog posts."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, description="Category name")
    slug: str = Field(unique=True, index=True, description="URL-friendly slug")
    description: Optional[str] = Field(default=None, description="Category description")
    color: Optional[str] = Field(default="#007bff", description="Category color for UI")
    is_active: bool = Field(default=True, description="Whether category is active")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Creation date"
    )

    # Relationships
    posts: List["Post"] = Relationship(back_populates="category")


class Tag(SQLModel, table=True):
    """Tag model for categorizing blog posts."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, description="Tag name")
    slug: str = Field(unique=True, index=True, description="URL-friendly slug")
    description: Optional[str] = Field(default=None, description="Tag description")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Creation date"
    )

    # Relationships
    posts: List["Post"] = Relationship(back_populates="tags", link_model="PostTag")


class PostTag(SQLModel, table=True):
    """Many-to-many relationship between Post and Tag."""

    post_id: Optional[int] = Field(
        default=None, foreign_key="post.id", primary_key=True
    )
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)


class Post(SQLModel, table=True):
    """Blog post model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, description="Post title")
    slug: str = Field(unique=True, index=True, description="URL-friendly slug")
    content: str = Field(description="Post content (markdown supported)")
    excerpt: Optional[str] = Field(default=None, description="Post excerpt/summary")
    featured_image: Optional[str] = Field(
        default=None, description="Featured image file path"
    )
    status: Literal["draft", "published", "archived"] = Field(
        default="draft", description="Post status"
    )
    is_featured: bool = Field(default=False, description="Whether post is featured")
    allow_comments: bool = Field(
        default=True, description="Whether comments are allowed"
    )
    view_count: int = Field(default=0, description="Number of views")
    published_at: Optional[datetime] = Field(
        default=None, description="Publication date"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Creation date"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Last update date"
    )

    # Foreign keys
    author_id: Optional[int] = Field(
        default=None, foreign_key="user.id", description="Post author"
    )
    category_id: Optional[int] = Field(
        default=None, foreign_key="category.id", description="Post category"
    )

    # Relationships
    author: Optional[BlogUser] = Relationship(back_populates="posts")
    category: Optional[Category] = Relationship(back_populates="posts")
    tags: List[Tag] = Relationship(back_populates="posts", link_model=PostTag)
    comments: List["Comment"] = Relationship(back_populates="post")


class Comment(SQLModel, table=True):
    """Comment model for blog posts."""

    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(description="Comment content")
    is_approved: bool = Field(default=False, description="Whether comment is approved")
    is_spam: bool = Field(
        default=False, description="Whether comment is marked as spam"
    )
    ip_address: Optional[str] = Field(
        default=None, description="Commenter's IP address"
    )
    user_agent: Optional[str] = Field(
        default=None, description="Commenter's user agent"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Comment date"
    )

    # Foreign keys
    post_id: Optional[int] = Field(
        default=None, foreign_key="post.id", description="Related post"
    )
    author_id: Optional[int] = Field(
        default=None, foreign_key="user.id", description="Comment author"
    )
    parent_id: Optional[int] = Field(
        default=None, foreign_key="comment.id", description="Parent comment for replies"
    )

    # Relationships
    post: Optional[Post] = Relationship(back_populates="comments")
    author: Optional[BlogUser] = Relationship(back_populates="comments")
    replies: List["Comment"] = Relationship(back_populates="parent")
    parent: Optional["Comment"] = Relationship(back_populates="replies")


class BlogSettings(SQLModel, table=True):
    """Blog settings and configuration."""

    id: Optional[int] = Field(default=None, primary_key=True)
    site_name: str = Field(default="My Blog", description="Blog site name")
    site_description: Optional[str] = Field(
        default=None, description="Blog description"
    )
    posts_per_page: int = Field(default=10, description="Number of posts per page")
    allow_registration: bool = Field(
        default=True, description="Allow user registration"
    )
    moderate_comments: bool = Field(
        default=True, description="Moderate comments before publishing"
    )
    auto_approve_comments: bool = Field(
        default=False, description="Auto-approve comments"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Last settings update"
    )
