"""
CRUD tests for blog models using fixtures.

This module tests all CRUD operations for blog models:
- Category
- Tag
- Post
- Comment
- Newsletter
- Analytics
- PostTagLink
"""

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.e2e


class TestCategoryCRUD:
    """Test CRUD operations for Category model."""

    def test_category_crud_operations(self, client: TestClient, tech_category) -> None:
        """Test full CRUD cycle for Category."""
        # Create category using fixture data
        category_data = {
            "data": {
                "name": tech_category.name,
                "slug": tech_category.slug,
                "description": tech_category.description,
                "is_active": tech_category.is_active,
            }
        }

        create_response = client.post("/api/v1/models/category", json=category_data)
        assert create_response.status_code == 200
        created_category = create_response.json()["data"]
        category_id = created_category["id"]

        # Read category
        read_response = client.get(f"/api/v1/models/category/{category_id}")
        assert read_response.status_code == 200
        read_category = read_response.json()["data"]
        assert read_category["name"] == tech_category.name
        assert read_category["slug"] == tech_category.slug

        # Update category
        update_data = {
            "data": {
                "description": "Updated technology description",
            }
        }
        update_response = client.put(
            f"/api/v1/models/category/{category_id}", json=update_data
        )
        assert update_response.status_code == 200
        updated_category = update_response.json()["data"]
        assert updated_category["description"] == "Updated technology description"

        # List categories
        list_response = client.get("/api/v1/models/category")
        assert list_response.status_code == 200
        categories = list_response.json()["data"]
        assert len(categories) > 0


class TestTagCRUD:
    """Test CRUD operations for Tag model."""

    def test_tag_crud_operations(self, client: TestClient, python_tag) -> None:
        """Test full CRUD cycle for Tag."""
        # Create tag using fixture data
        tag_data = {
            "data": {
                "name": python_tag.name,
                "slug": python_tag.slug,
                "description": python_tag.description,
                "usage_count": python_tag.usage_count,
            }
        }

        create_response = client.post("/api/v1/models/tag", json=tag_data)
        assert create_response.status_code == 200
        created_tag = create_response.json()["data"]
        tag_id = created_tag["id"]

        # Read tag
        read_response = client.get(f"/api/v1/models/tag/{tag_id}")
        assert read_response.status_code == 200
        read_tag = read_response.json()["data"]
        assert read_tag["name"] == python_tag.name
        assert read_tag["slug"] == python_tag.slug

        # Update tag
        update_data = {
            "data": {
                "description": "Updated Python description",
                "usage_count": 5,
            }
        }
        update_response = client.put(f"/api/v1/models/tag/{tag_id}", json=update_data)
        assert update_response.status_code == 200
        updated_tag = update_response.json()["data"]
        assert updated_tag["description"] == "Updated Python description"
        assert updated_tag["usage_count"] == 5

        # List tags
        list_response = client.get("/api/v1/models/tag")
        assert list_response.status_code == 200
        tags = list_response.json()["data"]
        assert len(tags) > 0

        # Note: DELETE operations are not implemented in the models API
        # The models API only supports GET, POST, and PUT operations


class TestPostCRUD:
    """Test CRUD operations for Post model."""

    def test_post_crud_operations(self, client: TestClient, sample_post) -> None:
        """Test full CRUD cycle for Post."""
        # First create a user for the author
        user_data = {
            "data": {
                "username": "blog_author",
                "email": "author@example.com",
                "password": "password123",
                "is_active": True,
                "is_superuser": False,
            }
        }
        user_response = client.post("/api/v1/models/user", json=user_data)
        assert user_response.status_code == 200
        user_id = user_response.json()["data"]["id"]

        # Create post using fixture data
        post_data = {
            "data": {
                "title": sample_post.title,
                "slug": sample_post.slug,
                "excerpt": sample_post.excerpt,
                "content": sample_post.content,
                "meta_description": sample_post.meta_description,
                "view_count": sample_post.view_count,
                "like_count": sample_post.like_count,
                "comment_count": sample_post.comment_count,
                "reading_time": sample_post.reading_time,
                "rating": sample_post.rating,
                "is_featured": sample_post.is_featured,
                "is_published": sample_post.is_published,
                "allow_comments": sample_post.allow_comments,
                "is_premium": sample_post.is_premium,
                "status": sample_post.status.value,
                "author_id": user_id,
            }
        }

        create_response = client.post("/api/v1/models/post", json=post_data)
        assert create_response.status_code == 200
        created_post = create_response.json()["data"]
        post_id = created_post["id"]

        # Read post
        read_response = client.get(f"/api/v1/models/post/{post_id}")
        assert read_response.status_code == 200
        read_post = read_response.json()["data"]
        assert read_post["title"] == sample_post.title
        assert read_post["slug"] == sample_post.slug

        # Update post
        update_data = {
            "data": {
                "title": "Updated Test Blog Post",
                "is_published": True,
                "status": "published",
                "view_count": 10,
            }
        }
        update_response = client.put(f"/api/v1/models/post/{post_id}", json=update_data)
        assert update_response.status_code == 200
        updated_post = update_response.json()["data"]
        assert updated_post["title"] == "Updated Test Blog Post"
        assert updated_post["is_published"] is True
        assert updated_post["status"] == "published"

        # List posts
        list_response = client.get("/api/v1/models/post")
        assert list_response.status_code == 200
        posts = list_response.json()["data"]
        assert len(posts) > 0

        # Note: DELETE operations are not implemented in the models API
        # The models API only supports GET, POST, and PUT operations


class TestCommentCRUD:
    """Test CRUD operations for Comment model."""

    def test_comment_crud_operations(self, client: TestClient, sample_comment) -> None:
        """Test full CRUD cycle for Comment."""
        # First create a user and post for the comment
        user_data = {
            "data": {
                "username": "comment_user",
                "email": "comment@example.com",
                "password": "password123",
                "is_active": True,
                "is_superuser": False,
            }
        }
        user_response = client.post("/api/v1/models/user", json=user_data)
        assert user_response.status_code == 200
        user_id = user_response.json()["data"]["id"]

        post_data = {
            "data": {
                "title": "Comment Test Post",
                "slug": "comment-test-post",
                "content": "Post content for comment testing",
                "author_id": user_id,
            }
        }
        post_response = client.post("/api/v1/models/post", json=post_data)
        assert post_response.status_code == 200
        post_id = post_response.json()["data"]["id"]

        # Create comment using fixture data
        comment_data = {
            "data": {
                "content": sample_comment.content,
                "author_name": sample_comment.author_name,
                "author_email": sample_comment.author_email,
                "author_website": sample_comment.author_website,
                "rating": sample_comment.rating,
                "is_approved": sample_comment.is_approved,
                "post_id": post_id,
                "user_id": user_id,
            }
        }

        create_response = client.post("/api/v1/models/comment", json=comment_data)
        assert create_response.status_code == 200
        created_comment = create_response.json()["data"]
        comment_id = created_comment["id"]

        # Read comment
        read_response = client.get(f"/api/v1/models/comment/{comment_id}")
        assert read_response.status_code == 200
        read_comment = read_response.json()["data"]
        assert read_comment["content"] == sample_comment.content
        assert read_comment["author_name"] == sample_comment.author_name

        # Update comment
        update_data = {
            "data": {
                "content": "Updated test comment",
                "is_approved": True,
                "rating": 5.0,
            }
        }
        update_response = client.put(
            f"/api/v1/models/comment/{comment_id}", json=update_data
        )
        assert update_response.status_code == 200
        updated_comment = update_response.json()["data"]
        assert updated_comment["content"] == "Updated test comment"
        assert updated_comment["is_approved"] is True
        assert updated_comment["rating"] == 5.0

        # List comments
        list_response = client.get("/api/v1/models/comment")
        assert list_response.status_code == 200
        comments = list_response.json()["data"]
        assert len(comments) > 0


class TestNewsletterCRUD:
    """Test CRUD operations for Newsletter model."""

    def test_newsletter_crud_operations(
        self, client: TestClient, sample_newsletter
    ) -> None:
        """Test full CRUD cycle for Newsletter."""
        # Create newsletter subscription using fixture data
        newsletter_data = {
            "data": {
                "email": sample_newsletter.email,
                "first_name": sample_newsletter.first_name,
                "last_name": sample_newsletter.last_name,
                "is_active": sample_newsletter.is_active,
                "is_verified": sample_newsletter.is_verified,
            }
        }

        create_response = client.post("/api/v1/models/newsletter", json=newsletter_data)
        assert create_response.status_code == 200
        created_newsletter = create_response.json()["data"]
        newsletter_id = created_newsletter["id"]

        # Read newsletter
        read_response = client.get(f"/api/v1/models/newsletter/{newsletter_id}")
        assert read_response.status_code == 200
        read_newsletter = read_response.json()["data"]
        assert read_newsletter["email"] == sample_newsletter.email
        assert read_newsletter["first_name"] == sample_newsletter.first_name

        # Update newsletter
        update_data = {
            "data": {
                "is_verified": True,
                "preferences": {"frequency": "weekly", "topics": ["tech", "news"]},
            }
        }
        update_response = client.put(
            f"/api/v1/models/newsletter/{newsletter_id}", json=update_data
        )
        assert update_response.status_code == 200
        updated_newsletter = update_response.json()["data"]
        assert updated_newsletter["is_verified"] is True

        # List newsletters
        list_response = client.get("/api/v1/models/newsletter")
        assert list_response.status_code == 200
        newsletters = list_response.json()["data"]
        assert len(newsletters) > 0

        # Note: DELETE operations are not implemented in the models API
        # The models API only supports GET, POST, and PUT operations


class TestAnalyticsCRUD:
    """Test CRUD operations for Analytics model."""

    def test_analytics_crud_operations(
        self, client: TestClient, sample_analytics_single
    ) -> None:
        """Test full CRUD cycle for Analytics."""
        # First create a user and post for analytics
        user_data = {
            "data": {
                "username": "analytics_user",
                "email": "analytics@example.com",
                "password": "password123",
                "is_active": True,
                "is_superuser": False,
            }
        }
        user_response = client.post("/api/v1/models/user", json=user_data)
        assert user_response.status_code == 200
        user_id = user_response.json()["data"]["id"]

        post_data = {
            "data": {
                "title": "Analytics Test Post",
                "slug": "analytics-test-post",
                "content": "Post content for analytics testing",
                "author_id": user_id,
            }
        }
        post_response = client.post("/api/v1/models/post", json=post_data)
        assert post_response.status_code == 200
        post_id = post_response.json()["data"]["id"]

        # Create analytics using fixture data
        analytics_data = {
            "data": {
                "page_url": sample_analytics_single.page_url,
                "user_agent": sample_analytics_single.user_agent,
                "ip_address": sample_analytics_single.ip_address,
                "referrer": sample_analytics_single.referrer,
                "session_duration": sample_analytics_single.session_duration,
                "scroll_depth": sample_analytics_single.scroll_depth,
                "is_bounce": sample_analytics_single.is_bounce,
                "post_id": post_id,
                "user_id": user_id,
            }
        }

        create_response = client.post("/api/v1/models/analytics", json=analytics_data)
        assert create_response.status_code == 200
        created_analytics = create_response.json()["data"]
        analytics_id = created_analytics["id"]

        # Read analytics
        read_response = client.get(f"/api/v1/models/analytics/{analytics_id}")
        assert read_response.status_code == 200
        read_analytics = read_response.json()["data"]
        assert read_analytics["page_url"] == sample_analytics_single.page_url
        assert read_analytics["ip_address"] == sample_analytics_single.ip_address

        # Update analytics
        update_data = {
            "data": {
                "session_duration": 180.0,
                "scroll_depth": 90.0,
                "is_bounce": False,
            }
        }
        update_response = client.put(
            f"/api/v1/models/analytics/{analytics_id}", json=update_data
        )
        assert update_response.status_code == 200
        updated_analytics = update_response.json()["data"]
        assert updated_analytics["session_duration"] == 180.0
        assert updated_analytics["scroll_depth"] == 90.0

        # List analytics
        list_response = client.get("/api/v1/models/analytics")
        assert list_response.status_code == 200
        analytics_list = list_response.json()["data"]
        assert len(analytics_list) > 0
