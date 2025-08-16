"""
End-to-end tests for the models API endpoints.
"""


def test_create_record_invalid_model(client):
    """Test creating record for non-existent model."""
    test_data = {"data": {"name": "Test"}, "form_id": "test_form_id"}

    response = client.post("/api/v1/models/nonexistentmodel", json=test_data)

    assert response.status_code == 404


def test_get_records(client):
    """Test getting records."""
    response = client.get("/api/v1/models/modeltest")

    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert "total" in result
    assert "page" in result
    assert "page_size" in result


def test_update_record_not_found(client):
    """Test updating non-existent record."""
    update_data = {"data": {"name": "Updated Name"}, "form_id": "test_form_id"}

    response = client.put("/api/v1/models/modeltest/999", json=update_data)

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]["errors"].lower()


def test_update_record_invalid_model(client):
    """Test updating record for non-existent model."""
    update_data = {"data": {"name": "Updated Name"}, "form_id": "test_form_id"}

    response = client.put("/api/v1/models/nonexistentmodel/1", json=update_data)

    assert response.status_code == 404


def test_create_record_with_non_exist_field(client):
    """Test creating record with invalid data."""
    payload = {
        "data": {
            "name": "Updated Name",
            "description": "description",
            "extra": "extra",
        },
        "form_id": "test_form",
    }
    response = client.post("/api/v1/models/modeltest", json=payload)

    assert response.status_code == 400


def test_get_record_by_id_not_found(client):
    """Test getting non-existent record by ID."""
    response = client.get("/api/v1/models/modeltest/999")

    assert response.status_code == 404
