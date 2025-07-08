import pytest
from fastapi.testclient import TestClient


@pytest.mark.e2e
def test_get_apps(client: TestClient) -> None:
    response = client.get("/api/v1/apps/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "auth",
            "label": "Authentication & Authorization",
            "models": [
                {"name": "user", "label": "Users", "url": "/api/v1/models/user"},
                {"name": "group", "label": "Groups", "url": "/api/v1/models/group"},
            ],
        }
    ]
