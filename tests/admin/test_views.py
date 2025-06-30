def test_get_views(client):
    response = client.get("/admin/v1/views/")
    assert response.status_code == 200
    assert response.json() == {
        "User": [
            {
                "fields": [
                    {
                        "error": None,
                        "field_type": "text",
                        "help_text": None,
                        "label": "Username",
                        "name": "username",
                        "options": None,
                    },
                    {
                        "error": None,
                        "field_type": "text",
                        "help_text": None,
                        "label": "Email",
                        "name": "email",
                        "options": None,
                    },
                    {
                        "error": None,
                        "field_type": "text",
                        "help_text": None,
                        "label": "Is Active",
                        "name": "is_active",
                        "options": None,
                    },
                ],
                "model": "User",
                "name": "UserForm",
                "view_type": "form",
            },
            {
                "default_form_id": "UserForm",
                "fields": [
                    {
                        "error": None,
                        "field_type": "text",
                        "help_text": None,
                        "label": "Id",
                        "name": "id",
                        "options": None,
                    },
                    {
                        "error": None,
                        "field_type": "text",
                        "help_text": None,
                        "label": "Username",
                        "name": "username",
                        "options": None,
                    },
                    {
                        "error": None,
                        "field_type": "text",
                        "help_text": None,
                        "label": "Email",
                        "name": "email",
                        "options": None,
                    },
                    {
                        "error": None,
                        "field_type": "text",
                        "help_text": None,
                        "label": "Password",
                        "name": "password",
                        "options": None,
                    },
                    {
                        "error": None,
                        "field_type": "checkbox",
                        "help_text": None,
                        "label": "Is active",
                        "name": "is_active",
                        "options": None,
                    },
                    {
                        "error": None,
                        "field_type": "checkbox",
                        "help_text": None,
                        "label": "Is superuser",
                        "name": "is_superuser",
                        "options": None,
                    },
                ],
                "model": "User",
                "name": "UserList",
                "view_type": "list",
            },
        ]
    }


def test_get_views_by_model(client):
    response = client.get("/admin/v1/views/User")
    assert response.status_code == 200
    assert response.json() == [
        {
            "fields": [
                {
                    "error": None,
                    "field_type": "text",
                    "help_text": None,
                    "label": "Username",
                    "name": "username",
                    "options": None,
                },
                {
                    "error": None,
                    "field_type": "text",
                    "help_text": None,
                    "label": "Email",
                    "name": "email",
                    "options": None,
                },
                {
                    "error": None,
                    "field_type": "text",
                    "help_text": None,
                    "label": "Is Active",
                    "name": "is_active",
                    "options": None,
                },
            ],
            "model": "User",
            "name": "UserForm",
            "view_type": "form",
        },
        {
            "default_form_id": "UserForm",
            "fields": [
                {
                    "error": None,
                    "field_type": "text",
                    "help_text": None,
                    "label": "Id",
                    "name": "id",
                    "options": None,
                },
                {
                    "error": None,
                    "field_type": "text",
                    "help_text": None,
                    "label": "Username",
                    "name": "username",
                    "options": None,
                },
                {
                    "error": None,
                    "field_type": "text",
                    "help_text": None,
                    "label": "Email",
                    "name": "email",
                    "options": None,
                },
                {
                    "error": None,
                    "field_type": "text",
                    "help_text": None,
                    "label": "Password",
                    "name": "password",
                    "options": None,
                },
                {
                    "error": None,
                    "field_type": "checkbox",
                    "help_text": None,
                    "label": "Is active",
                    "name": "is_active",
                    "options": None,
                },
                {
                    "error": None,
                    "field_type": "checkbox",
                    "help_text": None,
                    "label": "Is superuser",
                    "name": "is_superuser",
                    "options": None,
                },
            ],
            "model": "User",
            "name": "UserList",
            "view_type": "list",
        },
    ]
