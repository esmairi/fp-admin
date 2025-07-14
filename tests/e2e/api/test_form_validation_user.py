"""
Integration tests for form validation in API endpoints.

Tests the form validation functionality with form_id in the payload.
"""

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.e2e


class TestFormValidation:
    """Test cases for form validation in API endpoints."""

    def test_create_user_with_form_validation_missing_password(
        self, client: TestClient
    ) -> None:
        """Test creating user with form validation - missing password."""
        # Test data with form_id but missing password
        test_data = {
            "data": {
                "username": "testuser",
                "email": "test@example.com",
                "is_active": True,
                "is_superuser": False,
            },
            "form_id": "UserForm",
        }

        response = client.post("/api/v1/models/user", json=test_data)

        assert response.status_code == 400
        result = response.json()

        # Check that we get structured error response
        assert "detail" in result
        assert "errors" in result["detail"]
        assert "password" in result["detail"]["errors"]

    def test_create_user_with_form_validation_invalid_email(
        self, client: TestClient
    ) -> None:
        """Test creating user with form validation - invalid email."""
        test_data = {
            "data": {
                "username": "testuser",
                "email": "invalid-email-format",
                "password": "password123",
                "is_active": True,
                "is_superuser": False,
            },
            "form_id": "UserForm",
        }

        response = client.post("/api/v1/models/user", json=test_data)

        assert response.status_code == 400
        result = response.json()

        # Check that we get structured error response for email format
        assert "detail" in result
        assert "errors" in result["detail"]
        assert "email" in result["detail"]["errors"]

    def test_create_user_with_form_validation_success(self, client: TestClient) -> None:
        """Test creating user with form validation - success case."""
        test_data = {
            "data": {
                "username": "success_user",
                "email": "success@example.com",
                "password": "password123",
                "is_active": True,
                "is_superuser": False,
            },
            "form_id": "UserForm",
        }

        response = client.post("/api/v1/models/user", json=test_data)

        assert response.status_code == 200
        result = response.json()

        # Check that we get successful response
        assert "data" in result
        assert result["data"]["username"] == "success_user"
        assert result["data"]["email"] == "success@example.com"

    def test_create_user_without_form_validation(self, client: TestClient) -> None:
        """Test creating user without form validation (backward compatibility)."""
        test_data = {
            "data": {
                "username": "no_form_user",
                "email": "noform@example.com",
                "password": "password123",
                "is_active": True,
                "is_superuser": False,
            }
            # No form_id provided
        }

        response = client.post("/api/v1/models/user", json=test_data)

        # Should still work (no validation applied)
        assert response.status_code == 200
        result = response.json()
        assert "data" in result

    def test_create_user_invalid_form_id(self, client: TestClient) -> None:
        """Test creating user with invalid form_id."""
        test_data = {
            "data": {
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "is_active": True,
                "is_superuser": False,
            },
            "form_id": "nonexistent_form",
        }

        response = client.post("/api/v1/models/user", json=test_data)

        assert response.status_code == 400
        result = response.json()

        # Check that we get error for invalid form_id
        assert "detail" in result
        assert "errors" in result["detail"]

    def test_create_user_multiple_validation_errors(self, client: TestClient) -> None:
        """Test creating user with multiple validation errors."""
        test_data = {
            "data": {
                "username": "ab",
                "email": "invalid-email",  # Invalid format
                "password": "123",  # Too short
                "is_active": "not boolean",  # Wrong type
                "is_superuser": False,
            },
            "form_id": "UserForm",
        }

        response = client.post("/api/v1/models/user", json=test_data)

        assert response.status_code == 400
        result = response.json()

        # Check that we get multiple field errors
        assert "detail" in result
        assert "errors" in result["detail"]
        error_fields = result["detail"]["errors"]

        # Should have errors for multiple fields
        assert len(error_fields) >= 3
        assert "email" in error_fields and "password" in error_fields
