# Views API

This guide covers the Views API endpoints in fp-admin for retrieving admin view configurations.

## Overview

The Views API provides endpoints to discover and retrieve admin view configurations. Views define how models are displayed and edited in the admin interface, including form fields, list displays, and validation rules.

## Base URL

```
GET /admin/api/v1/views/
```

## Endpoints

### List All Views

Retrieve all registered views organized by model name.

**Endpoint:** `GET /admin/api/v1/views/`

**Response:** `ViewsResponseSchema`

**Example Request:**
```bash
curl -X GET "http://localhost:8000/admin/api/v1/views/" \
  -H "accept: application/json"
```

**Example Response:**
```json
{
  "data": {
    "user": [
      {
        "name": "UserForm",
        "view_type": "form",
        "model": "User",
        "fields": [
          {
            "name": "id",
            "title": "ID",
            "field_type": "primarykey",
            "required": false,
            "readonly": true,
            "disabled": true,
            "is_primary_key": true
          },
          {
            "name": "username",
            "title": "Username",
            "field_type": "string",
            "required": true,
            "readonly": false,
            "disabled": false,
            "placeholder": "Enter username"
          },
          {
            "name": "email",
            "title": "Email",
            "field_type": "string",
            "required": true,
            "readonly": false,
            "disabled": false,
            "placeholder": "Enter email"
          },
          {
            "name": "password",
            "title": "Password",
            "field_type": "string",
            "widget": "password",
            "required": true,
            "readonly": false,
            "disabled": false
          },
          {
            "name": "is_active",
            "title": "Active",
            "field_type": "boolean",
            "required": false,
            "readonly": false,
            "disabled": false,
            "default_value": true
          },
          {
            "name": "is_superuser",
            "title": "Superuser",
            "field_type": "boolean",
            "required": false,
            "readonly": false,
            "disabled": false,
            "default_value": false
          }
        ],
        "creation_fields": ["username", "email", "password", "is_active", "is_superuser"],
        "allowed_update_fields": ["email", "is_active", "is_superuser"]
      },
      {
        "name": "UserList",
        "view_type": "list",
        "model": "User",
        "fields": [
          {
            "name": "id",
            "title": "ID",
            "field_type": "primarykey",
            "required": false,
            "readonly": true,
            "disabled": true,
            "is_primary_key": true
          },
          {
            "name": "username",
            "title": "Username",
            "field_type": "string",
            "required": false,
            "readonly": false,
            "disabled": false
          },
          {
            "name": "email",
            "title": "Email",
            "field_type": "string",
            "required": false,
            "readonly": false,
            "disabled": false
          },
          {
            "name": "is_active",
            "title": "Active",
            "field_type": "boolean",
            "required": false,
            "readonly": false,
            "disabled": false
          },
          {
            "name": "is_superuser",
            "title": "Superuser",
            "field_type": "boolean",
            "required": false,
            "readonly": false,
            "disabled": false
          }
        ]
      }
    ],
    "group": [
      {
        "name": "GroupForm",
        "view_type": "form",
        "model": "Group",
        "fields": [
          {
            "name": "id",
            "title": "ID",
            "field_type": "primarykey",
            "required": false,
            "readonly": true,
            "disabled": true,
            "is_primary_key": true
          },
          {
            "name": "name",
            "title": "Name",
            "field_type": "string",
            "required": true,
            "readonly": false,
            "disabled": false,
            "placeholder": "Enter group name"
          },
          {
            "name": "description",
            "title": "Description",
            "field_type": "string",
            "required": true,
            "readonly": false,
            "disabled": false,
            "placeholder": "Enter description"
          }
        ],
        "creation_fields": ["name", "description"],
        "allowed_update_fields": ["name", "description"]
      }
    ]
  }
}
```

### Get Model Views

Retrieve all views for a specific model.

**Endpoint:** `GET /admin/api/v1/views/{model_name}/`

**Response:** `ModelViewsResponseSchema`

**Example Request:**
```bash
curl -X GET "http://localhost:8000/admin/api/v1/views/user/" \
  -H "accept: application/json"
```

**Example Response:**
```json
{
  "data": [
    {
      "name": "UserForm",
      "view_type": "form",
      "model": "User",
      "fields": [
        {
          "name": "id",
          "title": "ID",
          "field_type": "primarykey",
          "required": false,
          "readonly": true,
          "disabled": true,
          "is_primary_key": true
        },
        {
          "name": "username",
          "title": "Username",
          "field_type": "string",
          "required": true,
          "readonly": false,
          "disabled": false,
          "placeholder": "Enter username"
        },
        {
          "name": "email",
          "title": "Email",
          "field_type": "string",
          "required": true,
          "readonly": false,
          "disabled": false,
          "placeholder": "Enter email"
        },
        {
          "name": "password",
          "title": "Password",
          "field_type": "string",
          "widget": "password",
          "required": true,
          "readonly": false,
          "disabled": false
        },
        {
          "name": "is_active",
          "title": "Active",
          "field_type": "boolean",
          "required": false,
          "readonly": false,
          "disabled": false,
          "default_value": true
        },
        {
          "name": "is_superuser",
          "title": "Superuser",
          "field_type": "boolean",
          "required": false,
          "readonly": false,
          "disabled": false,
          "default_value": false
        }
      ],
      "creation_fields": ["username", "email", "password", "is_active", "is_superuser"],
      "allowed_update_fields": ["email", "is_active", "is_superuser"]
    },
    {
      "name": "UserList",
      "view_type": "list",
      "model": "User",
      "fields": [
        {
          "name": "id",
          "title": "ID",
          "field_type": "primarykey",
          "required": false,
          "readonly": true,
          "disabled": true,
          "is_primary_key": true
        },
        {
          "name": "username",
          "title": "Username",
          "field_type": "string",
          "required": false,
          "readonly": false,
          "disabled": false
        },
        {
          "name": "email",
          "title": "Email",
          "field_type": "string",
          "required": false,
          "readonly": false,
          "disabled": false
        },
        {
          "name": "is_active",
          "title": "Active",
          "field_type": "boolean",
          "required": false,
          "readonly": false,
          "disabled": false
        },
        {
          "name": "is_superuser",
          "title": "Superuser",
          "field_type": "boolean",
          "required": false,
          "readonly": false,
          "disabled": false
        }
      ]
    }
  ]
}
```

## Data Models

### ViewsResponseSchema

Response schema for the list all views endpoint.

| Field | Type | Description |
|-------|------|-------------|
| `data` | `Dict[str, List[BaseViewInstanceSchema]]` | Views organized by model name |

### ModelViewsResponseSchema

Response schema for the get model views endpoint.

| Field | Type | Description |
|-------|------|-------------|
| `data` | `List[BaseViewInstanceSchema]` | List of views for the specified model |

### BaseViewInstanceSchema

Union type for different view types.

**Types:**
- `FormViewSchema` - Form view configuration
- `ListViewSchema` - List view configuration

### FormViewSchema

Schema for form view configuration.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | View name |
| `view_type` | `"form"` | View type (always "form") |
| `model` | `string` | Model name |
| `fields` | `List[FieldViewSchema]` | Form fields configuration |
| `creation_fields` | `List[string]` | Fields allowed during creation |
| `allowed_update_fields` | `List[string]` | Fields allowed during updates |

### ListViewSchema

Schema for list view configuration.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | View name |
| `view_type` | `"list"` | View type (always "list") |
| `model` | `string` | Model name |
| `fields` | `List[FieldViewSchema]` | List fields configuration |

### FieldViewSchema

Schema for field configuration.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Field name |
| `title` | `string` | Field display title |
| `help_text` | `string` | Field help text |
| `field_type` | `string` | Field type (string, boolean, etc.) |
| `widget` | `string` | Widget type (text, password, etc.) |
| `required` | `boolean` | Whether field is required |
| `readonly` | `boolean` | Whether field is readonly |
| `disabled` | `boolean` | Whether field is disabled |
| `placeholder` | `string` | Field placeholder text |
| `default_value` | `any` | Field default value |
| `options` | `object` | Field options |
| `error` | `FieldErrorSchema` | Field error information |
| `is_primary_key` | `boolean` | Whether field is primary key |

### FieldErrorSchema

Schema for field error information.

| Field | Type | Description |
|-------|------|-------------|
| `message` | `string` | Error message |
| `code` | `string` | Error code |

## View Registration

Views are automatically registered when they follow the fp-admin view structure:

### Form View Registration

```python
from fp_admin.registry import ViewBuilder
from fp_admin.admin.fields import FieldFactory

class UserFormView(ViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("username", "Username", required=True),
        FieldFactory.email_field("email", "Email", required=True),
        FieldFactory.password_field("password", "Password", required=True),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),
    ]

    creation_fields = ["username", "email", "password", "is_active", "is_superuser"]
    allowed_update_fields = ["email", "is_active", "is_superuser"]
```

### List View Registration

```python
class UserListView(BaseViewBuilder):
    model = User
    view_type = "list"
    name = "UserList"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("username", "Username"),
        FieldFactory.email_field("email", "Email"),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),
    ]
```

## API Usage Examples

### Get All Views

```python
import requests

# Get all views
response = requests.get("http://localhost:8000/admin/api/v1/views/")
views_data = response.json()

for model_name, views in views_data["data"].items():
    print(f"Model: {model_name}")
    for view in views:
        print(f"  View: {view['name']} ({view['view_type']})")
        print(f"  Fields: {len(view['fields'])}")
```

### Get Views for Specific Model

```python
import requests

# Get views for user model
response = requests.get("http://localhost:8000/admin/api/v1/views/user/")
user_views = response.json()

for view in user_views["data"]:
    print(f"View: {view['name']}")
    print(f"Type: {view['view_type']}")
    print(f"Fields: {[field['name'] for field in view['fields']]}")
```

### Find Form Views

```python
import requests

def get_form_views():
    """Get all form views."""
    response = requests.get("http://localhost:8000/admin/api/v1/views/")
    views_data = response.json()

    form_views = []
    for model_name, views in views_data["data"].items():
        for view in views:
            if view["view_type"] == "form":
                form_views.append({
                    "model": model_name,
                    "view": view
                })

    return form_views

# Usage
form_views = get_form_views()
for item in form_views:
    print(f"Form view for {item['model']}: {item['view']['name']}")
```

### Get Field Information

```python
import requests

def get_field_info(model_name: str, view_name: str):
    """Get field information for a specific view."""
    response = requests.get(f"http://localhost:8000/admin/api/v1/views/{model_name}/")
    views = response.json()

    for view in views["data"]:
        if view["name"] == view_name:
            return view["fields"]

    return None

# Usage
user_form_fields = get_field_info("user", "UserForm")
if user_form_fields:
    for field in user_form_fields:
        print(f"Field: {field['name']} ({field['field_type']})")
        print(f"  Required: {field['required']}")
        print(f"  Readonly: {field['readonly']}")
```

## Error Responses

### 404 Not Found

Returned when the views endpoint is not available or model not found.

```json
{
  "detail": "NOT FOUND"
}
```

### 500 Internal Server Error

Returned when there's an error retrieving view information.

```json
{
  "detail": "INTERNAL SERVER ERROR"
}
```

## Integration with Other APIs

### Models API Integration

The Views API works together with the Models API:

1. **Discover Views**: Use the Views API to find available views
2. **Get Model Data**: Use the Models API for CRUD operations
3. **Form Validation**: Use view field configurations for validation

### Example Integration

```python
import requests

def get_model_with_views(model_name: str):
    """Get model data with view configuration."""
    # Get views for the model
    views_response = requests.get(f"http://localhost:8000/admin/api/v1/views/{model_name}/")
    views = views_response.json()

    # Get model data
    models_response = requests.get(f"http://localhost:8000/admin/api/v1/models/{model_name}/")
    model_data = models_response.json()

    return {
        "model": model_data,
        "views": views["data"]
    }

# Usage
user_info = get_model_with_views("user")
print(f"Model: {user_info['model']['name']}")
print(f"Views: {[view['name'] for view in user_info['views']]}")
```

## Best Practices

### 1. Cache View Information

```python
import requests
from functools import lru_cache

@lru_cache(maxsize=1)
def get_views_info():
    """Cache views information to avoid repeated API calls."""
    response = requests.get("http://localhost:8000/admin/api/v1/views/")
    return response.json()

# Usage
views = get_views_info()
```

### 2. Handle Errors Gracefully

```python
import requests

def get_views_safe():
    """Get views with error handling."""
    try:
        response = requests.get("http://localhost:8000/admin/api/v1/views/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERROR FETCHING VIEWS: {e}")
        return {"data": {}}
```

### 3. Validate View Names

```python
def is_valid_view(model_name: str, view_name: str, views_info: dict):
    """Check if a view name is valid for a model."""
    model_views = views_info["data"].get(model_name, [])
    return any(view["name"] == view_name for view in model_views)

# Usage
views = get_views_safe()
if is_valid_view("user", "UserForm", views):
    print("USER FORM VIEW IS AVAILABLE")
```

## Testing

### Test Views API

```python
import pytest
import requests

def test_views_api():
    """Test the views API endpoint."""
    response = requests.get("http://localhost:8000/admin/api/v1/views/")

    assert response.status_code == 200
    views_data = response.json()

    # Check that data is a dict
    assert isinstance(views_data["data"], dict)

    # Check view structure
    for model_name, views in views_data["data"].items():
        assert isinstance(views, list)

        for view in views:
            assert "name" in view
            assert "view_type" in view
            assert "model" in view
            assert "fields" in view
            assert view["view_type"] in ["form", "list"]

def test_model_views_api():
    """Test the model views API endpoint."""
    response = requests.get("http://localhost:8000/admin/api/v1/views/user/")

    assert response.status_code == 200
    views_data = response.json()

    # Check that data is a list
    assert isinstance(views_data["data"], list)

    # Check that we have user views
    assert len(views_data["data"]) > 0

    # Check view structure
    for view in views_data["data"]:
        assert view["model"] == "User"
        assert "name" in view
        assert "view_type" in view
        assert "fields" in view
```

## Configuration

### API Version

The Views API version is configured in your settings:

```python
# settings.py
ADMIN_PATH = "/admin"
API_VERSION = "v1"
```

### View Registration

Views are automatically registered when they inherit from `ViewBuilder`:

```python
# views.py
from fp_admin.registry import ViewBuilder

class CustomFormView(ViewBuilder):
    model = CustomModel
    view_type = "form"
    name = "CustomForm"

    fields = [
        # Field definitions...
    ]
```

## Security

### Authentication

The Views API may require authentication depending on your configuration:

```python
import requests

# With authentication
headers = {
    "Authorization": "Bearer your-token-here"
}
response = requests.get("http://localhost:8000/admin/api/v1/views/", headers=headers)
```

### Rate Limiting

Consider implementing rate limiting for the Views API:

```python
# Example rate limiting configuration
RATE_LIMIT = {
    "views_api": {
        "requests_per_minute": 60,
        "burst": 10
    }
}
```

## Monitoring

### Health Checks

Monitor the Views API health:

```python
def check_views_api_health():
    """Check if the views API is healthy."""
    try:
        response = requests.get("http://localhost:8000/admin/api/v1/views/", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
```

### Metrics

Track API usage:

```python
import time

def track_views_api_usage():
    """Track views API response time and success rate."""
    start_time = time.time()

    try:
        response = requests.get("http://localhost:8000/admin/api/v1/views/")
        response_time = time.time() - start_time

        # Log metrics
        print(f"VIEWS API RESPONSE TIME: {response_time:.3f}s")
        print(f"VIEWS API STATUS: {response.status_code}")

        return response.status_code == 200
    except Exception as e:
        print(f"VIEWS API ERROR: {e}")
        return False
```

## Next Steps

- **[Models API](models.md)** - Learn about the Models API for data operations
- **[Apps API](apps.md)** - Discover the Apps API for application information
- **[Authentication](../user-guide/authentication.md)** - Set up authentication for API access
- **[Admin Models](../user-guide/admin-models.md)** - Configure admin interfaces
