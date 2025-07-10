import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.e2e


class TestAuthModelsCRUD:
    def test_create_update_user(self, client: TestClient, regular_user):
        # Create user
        user_data = {
            "data": {
                "username": regular_user.username,
                "email": regular_user.email,
                "password": regular_user.password,
                "is_active": regular_user.is_active,
                "is_superuser": regular_user.is_superuser,
            }
        }
        create_response = client.post("/api/v1/models/user", json=user_data)
        assert create_response.status_code == 200
        created = create_response.json()["data"]
        user_id = created["id"]
        # Update user
        update_data = {
            "data": {"email": "updated_user@example.com", "is_active": False}
        }
        update_response = client.put(f"/api/v1/models/user/{user_id}", json=update_data)
        assert update_response.status_code == 200
        updated = update_response.json()["data"]
        assert updated["email"] == "updated_user@example.com"
        assert updated["is_active"] is False

    def test_create_update_group(self, client: TestClient, user_group):
        group_data = {
            "data": {"name": user_group.name, "description": user_group.description}
        }
        create_response = client.post("/api/v1/models/group", json=group_data)
        assert create_response.status_code == 200
        created = create_response.json()["data"]
        group_id = created["id"]
        # Update group
        update_data = {"data": {"description": "Updated group description"}}
        update_response = client.put(
            f"/api/v1/models/group/{group_id}", json=update_data
        )
        assert update_response.status_code == 200
        updated = update_response.json()["data"]
        assert updated["description"] == "Updated group description"

    def test_create_update_permission(self, client: TestClient, read_permission):
        perm_data = {
            "data": {
                "codename": read_permission.codename,
                "name": read_permission.name,
                "description": read_permission.description,
            }
        }
        create_response = client.post("/api/v1/models/permission", json=perm_data)
        assert create_response.status_code == 200
        created = create_response.json()["data"]
        perm_id = created["id"]
        # Update permission
        update_data = {"data": {"description": "Updated permission description"}}
        update_response = client.put(
            f"/api/v1/models/permission/{perm_id}", json=update_data
        )
        assert update_response.status_code == 200
        updated = update_response.json()["data"]
        assert updated["description"] == "Updated permission description"

    def test_create_update_user_group_link(
        self, client: TestClient, regular_user, user_group
    ):
        # Create user
        user_data = {
            "data": {
                "username": regular_user.username,
                "email": regular_user.email,
                "password": regular_user.password,
                "is_active": regular_user.is_active,
                "is_superuser": regular_user.is_superuser,
            }
        }
        user_resp = client.post("/api/v1/models/user", json=user_data)
        user_id = user_resp.json()["data"]["id"]
        # Create group
        group_data = {
            "data": {"name": user_group.name, "description": user_group.description}
        }
        group_resp = client.post("/api/v1/models/group", json=group_data)
        group_id = group_resp.json()["data"]["id"]
        # Create link
        link_data = {"data": {"user_id": user_id, "group_id": group_id}}
        link_resp = client.post("/api/v1/models/usergrouplink", json=link_data)
        assert link_resp.status_code == 200
        link = link_resp.json()["data"]
        assert link["user_id"] == user_id
        assert link["group_id"] == group_id
        # Update not supported for link models (composite PK), so just test creation

    def test_create_update_group_permission_link(
        self, client: TestClient, user_group, read_permission
    ):
        # Create group
        group_data = {
            "data": {"name": user_group.name, "description": user_group.description}
        }
        group_resp = client.post("/api/v1/models/group", json=group_data)
        group_id = group_resp.json()["data"]["id"]
        # Create permission
        perm_data = {
            "data": {
                "codename": read_permission.codename,
                "name": read_permission.name,
                "description": read_permission.description,
            }
        }
        perm_resp = client.post("/api/v1/models/permission", json=perm_data)
        perm_id = perm_resp.json()["data"]["id"]
        # Create link
        link_data = {"data": {"group_id": group_id, "permission_id": perm_id}}
        link_resp = client.post("/api/v1/models/grouppermissionlink", json=link_data)
        assert link_resp.status_code == 200
        link = link_resp.json()["data"]
        assert link["group_id"] == group_id
        assert link["permission_id"] == perm_id
        # Update not supported for link models (composite PK), so just test creation
