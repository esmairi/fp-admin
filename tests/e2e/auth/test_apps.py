import pytest
from fastapi.testclient import TestClient


@pytest.mark.e2e
def test_get_apps(client: TestClient) -> None:
    response = client.get("/admin/v1/apps/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "label": "Authentication & Authorization",
            "models": [
                {"label": "User of App", "name": "User"},
                {"label": "Group of users", "name": "Group"},
            ],
            "name": "auth",
        }
    ]
