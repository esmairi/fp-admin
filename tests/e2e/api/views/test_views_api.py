"""
End-to-end tests for the views API endpoints.
"""


class TestViewsAPI:
    """Test cases for views API endpoints."""

    def test_get_model_views(self, client):
        response = client.get("/api/v1/views/modeltest")
        assert response.status_code == 200
        expected = {
            "data": [
                {
                    "allowed_update_fields": ["name", "description"],
                    "creation_fields": ["name", "description"],
                    "fields": [
                        {
                            "disabled": False,
                            "field_type": "primary_key",
                            "is_primary_key": True,
                            "name": "id",
                            "readonly": False,
                            "required": False,
                            "title": "ID",
                            "validators": [],
                            "widget": "text",
                        },
                        {
                            "disabled": False,
                            "field_type": "string",
                            "is_primary_key": False,
                            "name": "name",
                            "readonly": False,
                            "required": True,
                            "title": "Name",
                            "validators": [],
                            "widget": "textarea",
                        },
                        {
                            "disabled": False,
                            "field_type": "string",
                            "is_primary_key": False,
                            "name": "description",
                            "readonly": False,
                            "required": True,
                            "title": "Description",
                            "validators": [],
                            "widget": "textarea",
                        },
                    ],
                    "model": "modeltest",
                    "name": "test_form",
                    "view_type": "form",
                },
                {
                    "default_form_id": "test_form",
                    "fields": [
                        {
                            "disabled": False,
                            "field_type": "primary_key",
                            "is_primary_key": True,
                            "name": "id",
                            "readonly": False,
                            "required": False,
                            "title": "ID",
                            "validators": [],
                            "widget": "text",
                        },
                        {
                            "disabled": False,
                            "field_type": "string",
                            "is_primary_key": False,
                            "name": "name",
                            "readonly": False,
                            "required": False,
                            "title": "Name",
                            "validators": [],
                            "widget": "textarea",
                        },
                        {
                            "disabled": False,
                            "field_type": "string",
                            "is_primary_key": False,
                            "name": "description",
                            "readonly": False,
                            "required": False,
                            "title": "Description",
                            "validators": [],
                            "widget": "textarea",
                        },
                    ],
                    "model": "modeltest",
                    "name": "test_list",
                    "view_type": "list",
                },
            ]
        }
        assert response.json() == expected

    def test_get_model_views_not_found(self, client):
        """Test getting views for non-existent model."""
        response = client.get("/api/v1/views/nonexistentmodel")

        assert response.status_code == 200
        result = response.json()
        assert "data" in result
        assert len(result["data"]) == 0

    def test_view_fields_structure(self, client):
        """Test that view fields have correct structure."""
        response = client.get("/api/v1/views/modeltest")

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

    def test_view_serialization(self, client):
        """Test that views are properly serialized."""
        response = client.get("/api/v1/views/modeltest")

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
