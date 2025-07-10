"""
End-to-end tests for the models API endpoints.
"""

from tests.fixtures.models import ModelTest


def test_create_record_success(client, db_manager):
    """Test successful record creation."""
    # Test data
    test_data = {
        "data": {"name": "Test Record", "description": "This is a test record"}
    }

    # Make POST request
    response = client.post("/api/v1/models/modeltest", json=test_data)

    # Verify response
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert result["data"]["name"] == test_data["data"]["name"]
    assert result["data"]["description"] == test_data["data"]["description"]
    assert "id" in result["data"]


def test_create_record_invalid_model(client):
    """Test creating record for non-existent model."""
    test_data = {"data": {"name": "Test"}}

    response = client.post("/api/v1/models/nonexistentmodel", json=test_data)

    assert response.status_code == 400
    assert (
        "Failed to create nonexistentmodel record: Model " "[nonexistentmodel]"
    ) in response.json()["detail"]["detail"]


def test_create_record_invalid_data(client):
    """Test creating record with invalid data."""
    # Missing required field
    test_data = {"data": {"name": "Test"}}  # Missing description

    response = client.post("/api/v1/models/modeltest", json=test_data)

    assert response.status_code == 400
    assert "Failed to create" in response.json()["detail"]["detail"]


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
    update_data = {"data": {"name": "Updated Name"}}

    response = client.put("/api/v1/models/modeltest/999", json=update_data)

    assert response.status_code == 400
    assert "not found" in response.json()["detail"]["detail"]


def test_update_record_invalid_model(client):
    """Test updating record for non-existent model."""
    update_data = {"data": {"name": "Updated Name"}}

    response = client.put("/api/v1/models/nonexistentmodel/1", json=update_data)

    assert response.status_code == 400
    assert "not found in registry" in response.json()["detail"]["detail"]


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
    assert "One or more fields failed validation" in response.json()["detail"]["detail"]


def test_update_record_with_non_exist_field(client, session):
    """Test creating record with invalid data."""
    with session as _session:
        record = ModelTest(name="new name", description="new description")
        _session.add(record)
        _session.commit()
        _session.refresh(record)

        payload = {
            "data": {
                "name": "Updated Name",
                "description": "description",
                "extra": "extra",
            },
            "form_id": "test_form",
        }
        response = client.put(
            "/api/v1/models/modeltest/{}".format(record.id), json=payload
        )

        assert response.status_code == 400
        assert (
            "One or more fields failed validation"
            in response.json()["detail"]["detail"]
        )


def test_update_record_with_form_validation(client):
    """Test updating record with form validation."""
    # First create a record
    test_data = {
        "data": {"name": "Original Name", "description": "Original description"}
    }

    create_response = client.post("/api/v1/models/modeltest", json=test_data)
    assert create_response.status_code == 200
    created_record = create_response.json()["data"]
    record_id = created_record["id"]

    # Update with form validation
    update_data = {
        "data": {"name": "Updated Name", "description": "Updated description"},
        "form_id": "test_form",
    }

    response = client.put(f"/api/v1/models/modeltest/{record_id}", json=update_data)

    # Should work if form validation passes
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert result["data"]["name"] == update_data["data"]["name"]


def test_get_record_by_id(client):
    """Test getting record by ID."""
    # First create a record
    test_data = {
        "data": {
            "name": "Test Record for Get",
            "description": "This is a test record for get by ID",
        }
    }

    create_response = client.post("/api/v1/models/modeltest", json=test_data)
    assert create_response.status_code == 200
    created_record = create_response.json()["data"]
    record_id = created_record["id"]

    # Now get the record by ID
    response = client.get(f"/api/v1/models/modeltest/{record_id}")

    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert result["data"]["id"] == record_id
    assert result["data"]["name"] == test_data["data"]["name"]


def test_get_record_by_id_not_found(client):
    """Test getting non-existent record by ID."""
    response = client.get("/api/v1/models/modeltest/999")

    assert response.status_code == 404
