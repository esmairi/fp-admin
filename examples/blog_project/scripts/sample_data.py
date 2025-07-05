"""
Sample data script for the blog application.

This script populates the blog with sample data including users,
categories, tags, and posts for demonstration purposes.
Uses the User model from fp_admin.apps.auth.models.
"""

import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from blog_project.apps.blog.models import BlogSettings, Category, Comment, Post, Tag

from fp_admin.apps.auth.models import User
from fp_admin.core.database import db_manager


def create_sample_data():
    """Create sample data for the blog application."""

    with db_manager.get_session() as session:
        print("🌱 Creating sample blog data...")

        # Create users (using auth User model)
        print("👥 Creating users...")
        admin_user = User(
            username="admin",
            email="admin@example.com",
            password="admin123",  # In production, this should be hashed
            is_active=True,
            is_superuser=True,
        )

        author1 = User(
            username="john_doe",
            email="john@example.com",
            password="password123",
            is_active=True,
            is_superuser=False,
        )

        author2 = User(
            username="jane_smith",
            email="jane@example.com",
            password="password123",
            is_active=True,
            is_superuser=False,
        )

        reader1 = User(
            username="bob_wilson",
            email="bob@example.com",
            password="password123",
            is_active=True,
            is_superuser=False,
        )

        session.add_all([admin_user, author1, author2, reader1])
        session.commit()

        # Create categories
        print("📂 Creating categories...")
        tech_category = Category(
            name="Technology",
            slug="technology",
            description="Latest tech news and tutorials",
            color="#007bff",
        )

        lifestyle_category = Category(
            name="Lifestyle",
            slug="lifestyle",
            description="Health, wellness, and personal development",
            color="#28a745",
        )

        programming_category = Category(
            name="Programming",
            slug="programming",
            description="Coding tutorials and development tips",
            color="#dc3545",
        )

        session.add_all([tech_category, lifestyle_category, programming_category])
        session.commit()

        # Create tags
        print("🏷️ Creating tags...")
        python_tag = Tag(
            name="Python", slug="python", description="Python programming language"
        )
        fastapi_tag = Tag(
            name="FastAPI", slug="fastapi", description="FastAPI web framework"
        )
        webdev_tag = Tag(
            name="Web Development",
            slug="web-development",
            description="Web development topics",
        )
        tutorial_tag = Tag(
            name="Tutorial", slug="tutorial", description="Step-by-step guides"
        )
        tips_tag = Tag(name="Tips", slug="tips", description="Helpful tips and tricks")

        session.add_all([python_tag, fastapi_tag, webdev_tag, tutorial_tag, tips_tag])
        session.commit()

        # Create posts
        print("📝 Creating posts...")

        post1 = Post(
            title="Getting Started with FastAPI",
            slug="getting-started-with-fastapi",
            content="# Getting Started with FastAPI\n\nFastAPI is a modern, fast web framework for building APIs with Python.",
            excerpt="Learn how to build modern APIs with FastAPI, a fast web framework for Python.",
            status="published",
            is_featured=True,
            allow_comments=True,
            author_id=author1.id,
            category_id=programming_category.id,
            published_at=datetime.now(UTC) - timedelta(days=5),
        )

        post2 = Post(
            title="Python Best Practices for 2024",
            slug="python-best-practices-2024",
            content="# Python Best Practices for 2024\n\nPython continues to evolve, and so do the best practices for writing clean, maintainable code.",
            excerpt="Discover the latest Python best practices to write cleaner, more maintainable code in 2024.",
            status="published",
            is_featured=False,
            allow_comments=True,
            author_id=author2.id,
            category_id=programming_category.id,
            published_at=datetime.now(UTC) - timedelta(days=3),
        )

        post3 = Post(
            title="Building a Blog with FastAPI Admin",
            slug="building-blog-fastapi-admin",
            content="# Building a Blog with FastAPI Admin\n\nFastAPI Admin provides a powerful admin interface for your FastAPI applications.",
            excerpt="Learn how to build a complete blog system using FastAPI Admin with user management, content management, and more.",
            status="published",
            is_featured=True,
            allow_comments=True,
            author_id=admin_user.id,
            category_id=tech_category.id,
            published_at=datetime.now(UTC) - timedelta(days=1),
        )

        session.add_all([post1, post2, post3])
        session.commit()

        # Add tags to posts
        post1.tags = [python_tag, fastapi_tag, tutorial_tag]
        post2.tags = [python_tag, tips_tag]
        post3.tags = [fastapi_tag, webdev_tag, tutorial_tag]
        session.commit()

        # Create comments
        print("💬 Creating comments...")

        comment1 = Comment(
            content="Great tutorial! FastAPI is really easy to get started with.",
            is_approved=True,
            author_id=reader1.id,
            post_id=post1.id,
        )

        comment2 = Comment(
            content="Thanks for sharing these best practices. Type hints are indeed very helpful!",
            is_approved=True,
            author_id=author1.id,
            post_id=post2.id,
        )

        comment3 = Comment(
            content="This looks amazing! Can't wait to try FastAPI Admin for my next project.",
            is_approved=True,
            author_id=reader1.id,
            post_id=post3.id,
        )

        session.add_all([comment1, comment2, comment3])
        session.commit()

        # Create blog settings
        print("⚙️ Creating blog settings...")
        blog_settings = BlogSettings(
            site_name="My Awesome Blog",
            site_description="A blog about technology, programming, and lifestyle",
            posts_per_page=10,
            allow_registration=True,
            moderate_comments=True,
            auto_approve_comments=False,
        )

        session.add(blog_settings)
        session.commit()

        print("✅ Sample data created successfully!")
        print("📊 Created:")
        print(f"   - {session.query(User).count()} users")
        print(f"   - {session.query(Category).count()} categories")
        print(f"   - {session.query(Tag).count()} tags")
        print(f"   - {session.query(Post).count()} posts")
        print(f"   - {session.query(Comment).count()} comments")
        print(f"   - {session.query(BlogSettings).count()} settings record")
        print()
        print("🚀 You can now:")
        print("   1. Run the application: python app.py")
        print("   2. Visit the admin interface")
        print("   3. Login with admin@example.com / admin123")
        print("   4. Explore the sample data")


if __name__ == "__main__":
    create_sample_data()
