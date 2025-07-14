"""
Integration test for the update endpoint using existing auth models.
"""

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.e2e


class TestUpdateIntegration:
    """Test cases for update endpoint integration."""

    def test_create__update_user_record(self, client: TestClient) -> None:
        """Test updating a user record."""
        # First create a user
        user_data = {
            "data": {
                "username": "testuser_update",
                "email": "test@example.com",
                "password": "password123",
                "is_active": True,
                "is_superuser": False,
            }
        }

        create_response = client.post("/api/v1/models/user", json=user_data)
        assert create_response.status_code == 200

        created_user = create_response.json()["data"]
        user_id = created_user["id"]

        # Update the user
        update_data = {
            "data": {
                "email": "updated@example.com",
                "is_active": False,
            }
        }

        response = client.put(f"/api/v1/models/user/{user_id}", json=update_data)

        # Verify response
        assert response.status_code == 200
        result = response.json()
        assert "data" in result
        assert result["data"]["email"] == "updated@example.com"
        assert result["data"]["is_active"] is False
        assert result["data"]["id"] == user_id

    def test_update_user_not_found(self, client: TestClient) -> None:
        """Test updating non-existent user."""
        update_data = {"data": {"email": "updated@example.com"}}

        response = client.put("/api/v1/models/user/100", json=update_data)

        assert response.status_code == 400
        assert "not found" in response.json()["detail"]["detail"]

    def test_update_user_with_form_validation(self, client: TestClient) -> None:
        """Test updating user with form validation."""
        # First create a user
        user_data = {
            "data": {
                "email": "formtest@example.com",
                "username": "testuser_create",
                "password": "<PASSWORD>",
                "is_active": True,
                "is_superuser": False,
            }
        }

        create_response = client.post("/api/v1/models/user", json=user_data)
        assert create_response.status_code == 200

        created_user = create_response.json()["data"]
        user_id = created_user["id"]

        # Update with form validation
        update_data = {
            "data": {
                "email": "formupdated@example.com",
                "is_active": False,
            },
            "form_id": "UserForm",
        }

        response = client.put(f"/api/v1/models/user/{user_id}", json=update_data)

        # Should work if form validation passes
        assert response.status_code == 200
        result = response.json()
        assert "data" in result
        assert result["data"]["username"] == "testuser_create"
        assert result["data"]["email"] == "formupdated@example.com"
