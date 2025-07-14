"""
End-to-end tests for the apps API endpoints.
"""


def test_apps_response(client):
    """Test that the /api/v1/apps/ endpoint returns the expected response structure."""
    response = client.get("/api/v1/apps/")
    assert response.status_code == 200

    # Assert the whole response
    assert response.json() == [
        {
            "name": "auth",
            "label": "Authentication & Authorization",
            "models": [
                {"name": "user", "label": "Users", "url": "/api/v1/models/user"},
                {"name": "group", "label": "Groups", "url": "/api/v1/models/group"},
                {
                    "name": "permission",
                    "label": "Permissions",
                    "url": "/api/v1/models/permission",
                },
                {
                    "name": "grouppermissionlink",
                    "label": "GroupPermissionLink",
                    "url": "/api/v1/models/grouppermissionlink",
                },
                {
                    "name": "usergrouplink",
                    "label": "UserGroupLink",
                    "url": "/api/v1/models/usergrouplink",
                },
            ],
        },
        {
            "name": "blog",
            "label": "Blog",
            "models": [
                {
                    "name": "category",
                    "label": "Categories",
                    "url": "/api/v1/models/category",
                },
                {"name": "tag", "label": "Tags", "url": "/api/v1/models/tag"},
                {"name": "post", "label": "Posts", "url": "/api/v1/models/post"},
                {
                    "name": "comment",
                    "label": "Comments",
                    "url": "/api/v1/models/comment",
                },
                {
                    "name": "newsletter",
                    "label": "Newsletter Subscriptions",
                    "url": "/api/v1/models/newsletter",
                },
                {
                    "name": "analytics",
                    "label": "Analytics",
                    "url": "/api/v1/models/analytics",
                },
                {
                    "name": "posttaglink",
                    "label": "PostTagLink",
                    "url": "/api/v1/models/posttaglink",
                },
            ],
        },
    ]
