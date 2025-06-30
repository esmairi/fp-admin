def test_get_apps(client):
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
