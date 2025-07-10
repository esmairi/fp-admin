import pytest

from tests.fixtures.apps.blog.models import (
    Analytics,
    Category,
    Comment,
    Newsletter,
    Post,
    PostStatus,
    Tag,
)


# Blog Fixtures
@pytest.fixture
def sample_categories():
    """Sample categories for testing."""
    return [
        Category(
            name="Technology",
            slug="technology",
            description="Technology related posts",
            color="#007bff",
            is_active=True,
        ),
        Category(
            name="Programming",
            slug="programming",
            description="Programming tutorials and guides",
            color="#28a745",
            is_active=True,
        ),
        Category(
            name="Design",
            slug="design",
            description="Design and UX articles",
            color="#dc3545",
            is_active=True,
        ),
    ]


@pytest.fixture
def sample_tags():
    """Sample tags for testing."""
    return [
        Tag(
            name="python",
            slug="python",
            description="Python programming language",
            usage_count=0,
        ),
        Tag(
            name="javascript",
            slug="javascript",
            description="JavaScript programming",
            usage_count=0,
        ),
        Tag(
            name="tutorial",
            slug="tutorial",
            description="Tutorial posts",
            usage_count=0,
        ),
        Tag(
            name="beginner",
            slug="beginner",
            description="Beginner friendly content",
            usage_count=0,
        ),
    ]


@pytest.fixture
def sample_posts():
    """Sample posts for testing."""
    return [
        Post(
            title="Getting Started with Python",
            slug="getting-started-python",
            excerpt="Learn the basics of Python programming",
            content="Python is a powerful programming language...",
            meta_description="Learn Python programming basics",
            view_count=0,
            like_count=0,
            comment_count=0,
            reading_time=5.0,
            rating=4.5,
            is_featured=False,
            is_published=True,
            allow_comments=True,
            is_premium=False,
            status=PostStatus.PUBLISHED,
            featured_image=None,
            attachments=None,
            seo_data={"keywords": "python, programming"},
            custom_fields={"difficulty": "beginner"},
            author_id=1,  # Will be set by test
        ),
        Post(
            title="Advanced JavaScript Patterns",
            slug="advanced-javascript-patterns",
            excerpt="Master advanced JavaScript concepts",
            content="JavaScript has evolved significantly...",
            meta_description="Advanced JavaScript patterns and techniques",
            view_count=0,
            like_count=0,
            comment_count=0,
            reading_time=8.0,
            rating=4.8,
            is_featured=True,
            is_published=True,
            allow_comments=True,
            is_premium=True,
            status=PostStatus.PUBLISHED,
            featured_image="/images/js-patterns.jpg",
            attachments=None,
            seo_data={"keywords": "javascript, patterns, advanced"},
            custom_fields={"difficulty": "advanced"},
            author_id=1,  # Will be set by test
        ),
    ]


@pytest.fixture
def sample_comments():
    """Sample comments for testing."""
    return [
        Comment(
            content="Great article! Very helpful for beginners.",
            author_name="John Doe",
            author_email="john@example.com",
            author_website="https://johndoe.com",
            rating=5.0,
            is_approved=False,
            is_spam=False,
            post_id=1,  # Will be set by test
        ),
        Comment(
            content="I found this really useful. Thanks for sharing!",
            author_name="Jane Smith",
            author_email="jane@example.com",
            author_website=None,
            rating=4.5,
            is_approved=True,
            is_spam=False,
            post_id=1,  # Will be set by test
        ),
    ]


@pytest.fixture
def sample_newsletters():
    """Sample newsletter subscriptions for testing."""
    return [
        Newsletter(
            email="subscriber1@example.com",
            first_name="Alice",
            last_name="Johnson",
            is_active=True,
            is_verified=False,
            preferences={"frequency": "weekly", "topics": ["tech", "news"]},
        ),
        Newsletter(
            email="subscriber2@example.com",
            first_name="Bob",
            last_name="Wilson",
            is_active=True,
            is_verified=True,
            preferences={"frequency": "daily", "topics": ["programming", "tutorials"]},
        ),
    ]


@pytest.fixture
def sample_analytics():
    """Sample analytics data for testing."""
    return [
        Analytics(
            page_url="/blog/getting-started-python",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            ip_address="192.168.1.1",
            referrer="https://google.com",
            session_duration=120.5,
            scroll_depth=75.0,
            is_bounce=False,
        ),
        Analytics(
            page_url="/blog/advanced-javascript-patterns",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            " AppleWebKit/537.36",
            ip_address="192.168.1.2",
            referrer="https://twitter.com",
            session_duration=300.0,
            scroll_depth=90.0,
            is_bounce=False,
        ),
    ]


@pytest.fixture
def tech_category():
    """Technology category fixture."""
    return Category(
        name="Technology",
        slug="technology",
        description="Technology related posts",
        color="#007bff",
        is_active=True,
    )


@pytest.fixture
def python_tag():
    """Python tag fixture."""
    return Tag(
        name="python",
        slug="python",
        description="Python programming language",
        usage_count=0,
    )


@pytest.fixture
def sample_post():
    """Sample post fixture."""
    return Post(
        title="Getting Started with Python",
        slug="getting-started-python",
        excerpt="Learn the basics of Python programming",
        content="Python is a powerful programming language...",
        meta_description="Learn Python programming basics",
        view_count=0,
        like_count=0,
        comment_count=0,
        reading_time=5.0,
        rating=4.5,
        is_featured=False,
        is_published=True,
        allow_comments=True,
        is_premium=False,
        status=PostStatus.PUBLISHED,
        featured_image=None,
        attachments=None,
        seo_data={"keywords": "python, programming"},
        custom_fields={"difficulty": "beginner"},
        author_id=1,  # Will be set by test
    )


@pytest.fixture
def sample_comment():
    """Sample comment fixture."""
    return Comment(
        content="Great article! Very helpful for beginners.",
        author_name="John Doe",
        author_email="john@example.com",
        author_website="https://johndoe.com",
        rating=5.0,
        is_approved=False,
        is_spam=False,
        post_id=1,  # Will be set by test
    )


@pytest.fixture
def sample_newsletter():
    """Sample newsletter fixture."""
    return Newsletter(
        email="subscriber@example.com",
        first_name="Alice",
        last_name="Johnson",
        is_active=True,
        is_verified=False,
        preferences={"frequency": "weekly", "topics": ["tech", "news"]},
    )


@pytest.fixture
def sample_analytics_single():
    """Sample analytics fixture."""
    return Analytics(
        page_url="/blog/getting-started-python",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        ip_address="192.168.1.1",
        referrer="https://google.com",
        session_duration=120.5,
        scroll_depth=75.0,
        is_bounce=False,
        post_id=1,  # Will be set by test
    )


# Additional fixtures for edge cases and different scenarios
@pytest.fixture
def draft_post():
    """Draft post fixture for testing unpublished content."""
    return Post(
        title="Draft Post",
        slug="draft-post",
        excerpt="This is a draft post",
        content="Draft content...",
        meta_description="Draft post description",
        view_count=0,
        like_count=0,
        comment_count=0,
        reading_time=3.0,
        rating=0.0,
        is_featured=False,
        is_published=False,
        allow_comments=False,
        is_premium=False,
        status=PostStatus.DRAFT,
        featured_image=None,
        attachments=None,
        seo_data=None,
        custom_fields=None,
        author_id=1,  # Will be set by test
    )


@pytest.fixture
def premium_post():
    """Premium post fixture for testing premium content."""
    return Post(
        title="Premium Content",
        slug="premium-content",
        excerpt="This is premium content",
        content="Premium content here...",
        meta_description="Premium content description",
        view_count=0,
        like_count=0,
        comment_count=0,
        reading_time=10.0,
        rating=4.9,
        is_featured=True,
        is_published=True,
        allow_comments=True,
        is_premium=True,
        status=PostStatus.PUBLISHED,
        featured_image="/images/premium.jpg",
        attachments="/files/premium-guide.pdf",
        seo_data={"keywords": "premium, exclusive"},
        custom_fields={"access_level": "premium"},
        author_id=1,  # Will be set by test
    )


@pytest.fixture
def inactive_category():
    """Inactive category fixture for testing disabled categories."""
    return Category(
        name="Inactive Category",
        slug="inactive-category",
        description="This category is inactive",
        color="#6c757d",
        is_active=False,
    )


@pytest.fixture
def popular_tag():
    """Popular tag fixture with high usage count."""
    return Tag(
        name="popular",
        slug="popular",
        description="Popular tag with high usage",
        usage_count=150,
    )


@pytest.fixture
def spam_comment():
    """Spam comment fixture for testing spam detection."""
    return Comment(
        content="Buy cheap viagra now!",
        author_name="Spammer",
        author_email="spam@example.com",
        author_website="http://spam-site.com",
        rating=None,
        is_approved=False,
        is_spam=True,
        post_id=1,  # Will be set by test
    )


@pytest.fixture
def verified_newsletter():
    """Verified newsletter fixture for testing verified subscriptions."""
    return Newsletter(
        email="verified@example.com",
        first_name="Verified",
        last_name="User",
        is_active=True,
        is_verified=True,
        preferences={"frequency": "daily", "topics": ["all"]},
    )


@pytest.fixture
def bounce_analytics():
    """Bounce analytics fixture for testing bounce visits."""
    return Analytics(
        page_url="/blog/bounce-test",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        ip_address="192.168.1.100",
        referrer=None,
        session_duration=5.0,
        scroll_depth=10.0,
        is_bounce=True,
        post_id=1,  # Will be set by test
    )
