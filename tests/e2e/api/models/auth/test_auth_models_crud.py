import pytest
from fastapi.testclient import TestClient

from fp_admin.apps.auth.models import Group

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
            },
            "form_id": "UserForm",
        }
        create_response = client.post("/api/v1/models/user", json=user_data)
        assert create_response.status_code == 200
        created = create_response.json()["data"]
        user_id = created["id"]
        # Update user
        update_data = {
            "data": {"email": "updated_user@example.com", "is_active": False},
            "form_id": "UserForm",
        }
        update_response = client.put(f"/api/v1/models/user/{user_id}", json=update_data)
        assert update_response.status_code == 200
        updated = update_response.json()["data"]
        assert updated["email"] == "updated_user@example.com"
        assert updated["is_active"] is False

    def test_create_update_group(self, client: TestClient, user_group):
        group_data = {
            "data": {"name": user_group.name, "description": user_group.description},
            "form_id": "GroupForm",
        }
        create_response = client.post("/api/v1/models/group", json=group_data)
        assert create_response.status_code == 200
        created = create_response.json()["data"]
        group_id = created["id"]
        # Update group
        update_data = {
            "data": {"description": "Updated group description"},
            "form_id": "GroupForm",
        }
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
            },
            "form_id": "PermissionForm",
        }
        create_response = client.post("/api/v1/models/permission", json=perm_data)
        assert create_response.status_code == 200
        created = create_response.json()["data"]
        perm_id = created["id"]
        # Update permission
        update_data = {
            "data": {"description": "Updated permission description"},
            "form_id": "PermissionForm",
        }
        update_response = client.put(
            f"/api/v1/models/permission/{perm_id}", json=update_data
        )
        assert update_response.status_code == 200
        updated = update_response.json()["data"]
        assert updated["description"] == "Updated permission description"

    @pytest.mark.asyncio
    async def test_create_update_user_group_link(
        self, client: TestClient, regular_user, user_group, session
    ):
        # Create user
        user_data = {
            "data": {
                "username": regular_user.username,
                "email": regular_user.email,
                "password": regular_user.password,
                "is_active": regular_user.is_active,
                "is_superuser": regular_user.is_superuser,
            },
            "form_id": "UserForm",
        }
        user_resp = client.post("/api/v1/models/user", json=user_data)
        user_id = user_resp.json()["data"]["id"]
        # Create group
        group = Group(name=user_group.name, description=user_group.description)
        session.add(group)
        await session.commit()
        await session.refresh(group)
        group_data = {
            "data": {"users": [{"id": user_id}]},
            "form_id": "GroupForm",
        }
        group_resp = client.put(f"/api/v1/models/group/{group.id}", json=group_data)
        group_id = group_resp.json()["data"]["id"]
        assert group_resp.status_code == 200
        response_data = group_resp.json()["data"]
        assert response_data["users"][0]["id"] == user_id
        assert response_data["id"] == group_id

    def test_create_update_group_permission_link(
        self, client: TestClient, user_group, read_permission
    ):
        # Create group
        group_data = {
            "data": {"name": user_group.name, "description": user_group.description},
            "form_id": "GroupForm",
        }
        group_resp = client.post("/api/v1/models/group", json=group_data)
        group_id = group_resp.json()["data"]["id"]
        # Create permission
        perm_data = {
            "data": {
                "codename": read_permission.codename,
                "name": read_permission.name,
                "description": read_permission.description,
            },
            "form_id": "PermissionForm",
        }
        perm_resp = client.post("/api/v1/models/permission", json=perm_data)
        perm_id = perm_resp.json()["data"]["id"]
        # Create link
        group_data = {
            "data": {"permissions": [{"id": perm_id}]},
            "form_id": "GroupForm",
        }
        group_resp = client.put(f"/api/v1/models/group/{group_id}", json=group_data)

        assert group_resp.status_code == 200
        group_resp_json = group_resp.json()["data"]
        assert group_resp_json["id"] == group_id
        assert group_resp_json["permissions"][0]["id"] == perm_id
