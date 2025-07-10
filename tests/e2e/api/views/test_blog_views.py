"""
End-to-end tests for the blog views API endpoints.
"""


class TestBlogViewsAPI:
    """Test cases for blog views API endpoints."""

    def test_get_category_views(self, client):
        """Test getting views for Category model."""
        response = client.get("/api/v1/views/category")
        assert response.status_code == 200
        result = response.json()

        # Check that we have both form and list views
        assert len(result["data"]) == 2

        # Find form and list views
        form_view = None
        list_view = None
        for view in result["data"]:
            if view["view_type"] == "form":
                form_view = view
            elif view["view_type"] == "list":
                list_view = view

        assert form_view is not None
        assert list_view is not None

        # Check form view structure
        assert form_view["name"] == "CategoryForm"
        assert form_view["model"] == "category"
        assert form_view["view_type"] == "form"
        assert "creation_fields" in form_view
        assert "allowed_update_fields" in form_view

        # Check list view structure
        assert list_view["name"] == "CategoryList"
        assert list_view["model"] == "category"
        assert list_view["view_type"] == "list"
        assert "default_form_id" in list_view

    def test_get_tag_views(self, client):
        """Test getting views for Tag model."""
        response = client.get("/api/v1/views/tag")
        assert response.status_code == 200
        result = response.json()

        # Check that we have both form and list views
        assert len(result["data"]) == 2

        # Find form and list views
        form_view = None
        list_view = None
        for view in result["data"]:
            if view["view_type"] == "form":
                form_view = view
            elif view["view_type"] == "list":
                list_view = view

        assert form_view is not None
        assert list_view is not None

        # Check form view structure
        assert form_view["name"] == "TagForm"
        assert form_view["model"] == "tag"
        assert form_view["view_type"] == "form"

        # Check list view structure
        assert list_view["name"] == "TagList"
        assert list_view["model"] == "tag"
        assert list_view["view_type"] == "list"

    def test_get_post_views(self, client):
        """Test getting views for Post model."""
        response = client.get("/api/v1/views/post")
        assert response.status_code == 200
        result = response.json()

        # Check that we have both form and list views
        assert len(result["data"]) == 2

        # Find form and list views
        form_view = None
        list_view = None
        for view in result["data"]:
            if view["view_type"] == "form":
                form_view = view
            elif view["view_type"] == "list":
                list_view = view

        assert form_view is not None
        assert list_view is not None

        # Check form view structure
        assert form_view["name"] == "PostForm"
        assert form_view["model"] == "post"
        assert form_view["view_type"] == "form"

        # Check that Post form has all expected fields
        field_names = [field["name"] for field in form_view["fields"]]
        expected_fields = [
            "id",
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
            "created_at",
            "updated_at",
            "published_at",
            "scheduled_at",
            "status",
            "featured_image",
            "attachments",
            "seo_data",
            "custom_fields",
            "author_id",
            "category_id",
            "tags",
        ]

        for field_name in expected_fields:
            assert (
                field_name in field_names
            ), f"Field {field_name} not found in Post form"

        # Check list view structure
        assert list_view["name"] == "PostList"
        assert list_view["model"] == "post"
        assert list_view["view_type"] == "list"

    def test_get_comment_views(self, client):
        """Test getting views for Comment model."""
        response = client.get("/api/v1/views/comment")
        assert response.status_code == 200
        result = response.json()

        # Check that we have both form and list views
        assert len(result["data"]) == 2

        # Find form and list views
        form_view = None
        list_view = None
        for view in result["data"]:
            if view["view_type"] == "form":
                form_view = view
            elif view["view_type"] == "list":
                list_view = view

        assert form_view is not None
        assert list_view is not None

        # Check form view structure
        assert form_view["name"] == "CommentForm"
        assert form_view["model"] == "comment"
        assert form_view["view_type"] == "form"

        # Check that Comment form has all expected fields
        field_names = [field["name"] for field in form_view["fields"]]
        expected_fields = [
            "id",
            "content",
            "author_name",
            "author_email",
            "author_website",
            "rating",
            "is_approved",
            "is_spam",
            "created_at",
            "updated_at",
            "post_id",
            "parent_id",
            "user_id",
        ]

        for field_name in expected_fields:
            assert (
                field_name in field_names
            ), f"Field {field_name} not found in Comment form"

        # Check list view structure
        assert list_view["name"] == "CommentList"
        assert list_view["model"] == "comment"
        assert list_view["view_type"] == "list"

    def test_get_newsletter_views(self, client):
        """Test getting views for Newsletter model."""
        response = client.get("/api/v1/views/newsletter")
        assert response.status_code == 200
        result = response.json()

        # Check that we have both form and list views
        assert len(result["data"]) == 2

        # Find form and list views
        form_view = None
        list_view = None
        for view in result["data"]:
            if view["view_type"] == "form":
                form_view = view
            elif view["view_type"] == "list":
                list_view = view

        assert form_view is not None
        assert list_view is not None

        # Check form view structure
        assert form_view["name"] == "NewsletterForm"
        assert form_view["model"] == "newsletter"
        assert form_view["view_type"] == "form"

        # Check that Newsletter form has all expected fields
        field_names = [field["name"] for field in form_view["fields"]]
        expected_fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_verified",
            "subscribed_at",
            "verified_at",
            "preferences",
        ]

        for field_name in expected_fields:
            assert (
                field_name in field_names
            ), f"Field {field_name} not found in Newsletter form"

        # Check list view structure
        assert list_view["name"] == "NewsletterList"
        assert list_view["model"] == "newsletter"
        assert list_view["view_type"] == "list"

    def test_get_analytics_views(self, client):
        """Test getting views for Analytics model."""
        response = client.get("/api/v1/views/analytics")
        assert response.status_code == 200
        result = response.json()

        # Check that we have both form and list views
        assert len(result["data"]) == 2

        # Find form and list views
        form_view = None
        list_view = None
        for view in result["data"]:
            if view["view_type"] == "form":
                form_view = view
            elif view["view_type"] == "list":
                list_view = view

        assert form_view is not None
        assert list_view is not None

        # Check form view structure
        assert form_view["name"] == "AnalyticsForm"
        assert form_view["model"] == "analytics"
        assert form_view["view_type"] == "form"

        # Check that Analytics form has all expected fields
        field_names = [field["name"] for field in form_view["fields"]]
        expected_fields = [
            "id",
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

        for field_name in expected_fields:
            assert (
                field_name in field_names
            ), f"Field {field_name} not found in Analytics form"

        # Check list view structure
        assert list_view["name"] == "AnalyticsList"
        assert list_view["model"] == "analytics"
        assert list_view["view_type"] == "list"

    def test_get_posttaglink_views(self, client):
        """Test getting views for PostTagLink model."""
        response = client.get("/api/v1/views/posttaglink")
        assert response.status_code == 200
        result = response.json()

        # Check that we have both form and list views
        assert len(result["data"]) == 2

        # Find form and list views
        form_view = None
        list_view = None
        for view in result["data"]:
            if view["view_type"] == "form":
                form_view = view
            elif view["view_type"] == "list":
                list_view = view

        assert form_view is not None
        assert list_view is not None

        # Check form view structure
        assert form_view["name"] == "PostTagLinkForm"
        assert form_view["model"] == "posttaglink"
        assert form_view["view_type"] == "form"

        # Check that PostTagLink form has all expected fields
        field_names = [field["name"] for field in form_view["fields"]]
        expected_fields = ["post_id", "tag_id"]

        for field_name in expected_fields:
            assert (
                field_name in field_names
            ), f"Field {field_name} not found in PostTagLink form"

        # Check list view structure
        assert list_view["name"] == "PostTagLinkList"
        assert list_view["model"] == "posttaglink"
        assert list_view["view_type"] == "list"

    def test_blog_views_not_found(self, client):
        """Test getting views for non-existent blog model."""
        response = client.get("/api/v1/views/nonexistentblogmodel")
        assert response.status_code == 200
        result = response.json()
        assert "data" in result
        assert len(result["data"]) == 0

    def test_blog_view_fields_structure(self, client):
        """Test that blog view fields have correct structure."""
        response = client.get("/api/v1/views/post")
        assert response.status_code == 200
        result = response.json()
        view = result["data"][0]

        # Check that fields exist and have required structure
        assert "fields" in view
        fields = view["fields"]
        assert isinstance(fields, list)

        # Check field structure
        for field in fields:
            assert "name" in field
            assert "field_type" in field
            assert "required" in field
            assert "readonly" in field
            assert "disabled" in field
            assert "is_primary_key" in field
            assert "title" in field
            assert "widget" in field

    def test_blog_view_serialization(self, client):
        """Test that blog views are properly serialized."""
        response = client.get("/api/v1/views/post")
        assert response.status_code == 200
        result = response.json()
        view = result["data"][0]

        # Test that all required fields are present and properly typed
        assert isinstance(view["name"], str)
        assert isinstance(view["view_type"], str)
        assert isinstance(view["model"], str)
        assert isinstance(view["fields"], list)

        # Test field serialization
        for field in view["fields"]:
            assert isinstance(field["name"], str)
            assert isinstance(field["field_type"], str)
            assert isinstance(field["required"], bool)
            assert isinstance(field["readonly"], bool)
            assert isinstance(field["disabled"], bool)
            assert isinstance(field["is_primary_key"], bool)
            assert isinstance(field["title"], str)
            assert isinstance(field["widget"], str)

    def test_blog_view_field_types(self, client):
        """Test that blog views have correct field types."""
        response = client.get("/api/v1/views/post")
        assert response.status_code == 200
        result = response.json()
        form_view = None
        for view in result["data"]:
            if view["view_type"] == "form":
                form_view = view
                break

        assert form_view is not None

        # Check specific field types
        field_map = {field["name"]: field for field in form_view["fields"]}

        # Check primary key field
        assert field_map["id"]["field_type"] == "primarykey"
        assert field_map["id"]["is_primary_key"] is True

        # Check string fields
        string_fields = ["title", "slug", "excerpt", "content", "meta_description"]
        for field_name in string_fields:
            assert field_map[field_name]["field_type"] == "string"

        # Check number fields
        number_fields = ["view_count", "like_count", "comment_count"]
        for field_name in number_fields:
            assert field_map[field_name]["field_type"] == "number"

        # Check float fields
        assert field_map["reading_time"]["field_type"] == "float"
        assert field_map["rating"]["field_type"] == "number"

        # Check boolean fields
        boolean_fields = ["is_featured", "is_premium"]
        for field_name in boolean_fields:
            assert field_map[field_name]["field_type"] == "boolean"

        # Check datetime fields
        datetime_fields = ["created_at", "updated_at", "published_at", "scheduled_at"]
        for field_name in datetime_fields:
            assert field_map[field_name]["field_type"] == "datetime"

        # Check choice field
        assert field_map["status"]["field_type"] == "choice"

        # Check file fields
        file_fields = ["featured_image", "attachments"]
        for field_name in file_fields:
            assert field_map[field_name]["field_type"] == "file"

        # Check json fields
        json_fields = ["seo_data", "custom_fields"]
        for field_name in json_fields:
            assert field_map[field_name]["field_type"] == "json"

        # Check foreign key fields
        assert field_map["author_id"]["field_type"] == "foreignkey"
        assert field_map["category_id"]["field_type"] == "foreignkey"

        # Check many-to-many field
        assert field_map["tags"]["field_type"] == "many_to_many"

    def test_blog_view_relationships(self, client):
        """Test that blog views have correct relationship configurations."""
        response = client.get("/api/v1/views/post")
        assert response.status_code == 200
        result = response.json()
        form_view = None
        for view in result["data"]:
            if view["view_type"] == "form":
                form_view = view
                break

        assert form_view is not None
        field_map = {field["name"]: field for field in form_view["fields"]}

        # Check foreign key relationships
        author_field = field_map["author_id"]
        assert "options" in author_field
        assert author_field["options"]["field_title"] == "username"
        assert author_field["options"]["target_model"] == "user"

        category_field = field_map["category_id"]
        assert "options" in category_field
        assert category_field["options"]["field_title"] == "name"
        assert category_field["options"]["target_model"] == "category"

        # Check many-to-many relationships
        tags_field = field_map["tags"]
        assert "options" in tags_field
        assert tags_field["options"]["field_title"] == "name"
        assert tags_field["options"]["target_model"] == "tag"

    def test_blog_view_creation_fields(self, client):
        """Test that blog views have correct creation fields."""
        response = client.get("/api/v1/views/post")
        assert response.status_code == 200
        result = response.json()
        form_view = None
        for view in result["data"]:
            if view["view_type"] == "form":
                form_view = view
                break

        assert form_view is not None
        assert "creation_fields" in form_view
        creation_fields = form_view["creation_fields"]

        # Check that creation fields are properly configured
        assert isinstance(creation_fields, list)
        assert len(creation_fields) > 0

    def test_blog_view_update_fields(self, client):
        """Test that blog views have correct update fields."""
        response = client.get("/api/v1/views/post")
        assert response.status_code == 200
        result = response.json()
        form_view = None
        for view in result["data"]:
            if view["view_type"] == "form":
                form_view = view
                break

        assert form_view is not None
        assert "allowed_update_fields" in form_view
        update_fields = form_view["allowed_update_fields"]

        # Check that update fields are properly configured
        assert isinstance(update_fields, list)
        assert len(update_fields) > 0

    def test_all_blog_views(self, client):
        """Test getting all blog views."""
        response = client.get("/api/v1/views/")
        assert response.status_code == 200
        result = response.json()

        # Check that we have blog models in the response
        assert "data" in result
        data = result["data"]

        # Check for blog models
        blog_models = [
            "category",
            "tag",
            "post",
            "comment",
            "newsletter",
            "analytics",
            "posttaglink",
        ]
        for model_name in blog_models:
            if model_name in data:
                model_views = data[model_name]
                assert isinstance(model_views, list)
                assert len(model_views) > 0

                # Check that each model has at least one view
                for view in model_views:
                    assert "name" in view
                    assert "view_type" in view
                    assert "model" in view
                    assert "fields" in view
                    assert view["model"] == model_name
