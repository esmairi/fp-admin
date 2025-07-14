# Apps API

This guide covers the Apps API endpoints in fp-admin for managing and retrieving application information.

## Overview

The Apps API provides endpoints to discover and manage applications registered with fp-admin. It allows you to retrieve information about available apps, their models, and their configurations.

## Base URL

```
GET /admin/api/v1/apps/
```

## Endpoints

### List Applications

Retrieve a list of all registered applications with their models.

**Endpoint:** `GET /admin/api/v1/apps/`

**Response:** `List[AppInfo]`

**Example Request:**
```bash
curl -X GET "http://localhost:8000/admin/api/v1/apps/" \
  -H "accept: application/json"
```

**Example Response:**
```json
[
  {
    "name": "auth",
    "label": "Authentication & Authorization",
    "models": [
      {
        "name": "User",
        "label": "Users",
        "url": "/admin/api/v1/models/User"
      },
      {
        "name": "Group",
        "label": "Groups",
        "url": "/admin/api/v1/models/Group"
      },
      {
        "name": "Permission",
        "label": "Permissions",
        "url": "/admin/api/v1/models/Permission"
      }
    ]
  },
  {
    "name": "blog",
    "label": "Blog",
    "models": [
      {
        "name": "Post",
        "label": "Posts",
        "url": "/admin/api/v1/models/Post"
      },
      {
        "name": "Category",
        "label": "Categories",
        "url": "/admin/api/v1/models/Category"
      },
      {
        "name": "Tag",
        "label": "Tags",
        "url": "/admin/api/v1/models/Tag"
      }
    ]
  }
]
```

## Data Models

### AppInfo

Represents information about a registered application.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | The application name (e.g., "auth", "blog") |
| `label` | `string` | The human-readable application label |
| `models` | `List[ModelInfo]` | List of models available in this app |

### ModelInfo

Represents information about a model within an application.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | The model name (e.g., "User", "Post") |
| `label` | `string` | The human-readable model label |
| `url` | `string` | The API URL for this model's endpoints |

## Application Registration

Applications are automatically discovered and registered when they follow the fp-admin app structure:

### App Configuration

```python
# apps.py
from fp_admin.admin.apps import AppConfig

class AuthConfig(AppConfig):
    name = "auth"
    verbose_name = "Authentication & Authorization"
```

### Model Registration

```python
# admin.py
from fp_admin.admin.models import AdminModel
from .models import User, Group, Permission

class UserAdmin(AdminModel):
    model = User
    label = "Users"

class GroupAdmin(AdminModel):
    model = Group
    label = "Groups"

class PermissionAdmin(AdminModel):
    model = Permission
    label = "Permissions"
```

## API Usage Examples

### Get All Applications

```python
import requests

# Get all applications
response = requests.get("http://localhost:8000/admin/api/v1/apps/")
apps = response.json()

for app in apps:
    print(f"App: {app['name']} - {app['label']}")
    for model in app['models']:
        print(f"  Model: {model['name']} - {model['label']}")
```

### Find Specific Application

```python
import requests

# Get all applications
response = requests.get("http://localhost:8000/admin/api/v1/apps/")
apps = response.json()

# Find auth app
auth_app = next((app for app in apps if app['name'] == 'auth'), None)
if auth_app:
    print(f"Found auth app: {auth_app['label']}")
    print(f"Models: {[model['name'] for model in auth_app['models']]}")
```

### Get Models for Application

```python
import requests

# Get all applications
response = requests.get("http://localhost:8000/admin/api/v1/apps/")
apps = response.json()

# Get models for blog app
blog_app = next((app for app in apps if app['name'] == 'blog'), None)
if blog_app:
    for model in blog_app['models']:
        print(f"Model: {model['name']}")
        print(f"Label: {model['label']}")
        print(f"API URL: {model['url']}")
```

## Error Responses

### 404 Not Found

Returned when the apps endpoint is not available.

```json
{
  "detail": "NOT FOUND"
}
```

### 500 Internal Server Error

Returned when there's an error retrieving app information.

```json
{
  "detail": "INTERNAL SERVER ERROR"
}
```

## Integration with Other APIs

### Models API

The Apps API works together with the Models API:

1. **Discover Apps**: Use the Apps API to find available applications
2. **Get Model Details**: Use the model URLs from the Apps API to access the Models API
3. **CRUD Operations**: Use the Models API endpoints for data operations

### Example Integration

```python
import requests

def get_app_models(app_name):
    """Get all models for a specific application"""
    # Get apps
    apps_response = requests.get("http://localhost:8000/admin/api/v1/apps/")
    apps = apps_response.json()

    # Find the app
    app = next((app for app in apps if app['name'] == app_name), None)
    if not app:
        return None

    # Get model details
    models = []
    for model_info in app['models']:
        model_response = requests.get(f"http://localhost:8000{model_info['url']}")
        if model_response.status_code == 200:
            models.append(model_response.json())

    return models

# Usage
auth_models = get_app_models("auth")
blog_models = get_app_models("blog")
```

## Best Practices

### 1. Cache Application Information

```python
import requests
from functools import lru_cache

@lru_cache(maxsize=1)
def get_apps_info():
    """Cache apps information to avoid repeated API calls"""
    response = requests.get("http://localhost:8000/admin/api/v1/apps/")
    return response.json()

# Usage
apps = get_apps_info()
```

### 2. Handle Errors Gracefully

```python
import requests

def get_apps_safe():
    """Get apps with error handling"""
    try:
        response = requests.get("http://localhost:8000/admin/api/v1/apps/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERROR FETCHING APPS: {e}")
        return []
```

### 3. Validate Application Names

```python
def is_valid_app(app_name, apps_info):
    """Check if an app name is valid"""
    return any(app['name'] == app_name for app in apps_info)

# Usage
apps = get_apps_safe()
if is_valid_app("auth", apps):
    print("AUTH APP IS AVAILABLE")
```

## Testing

### Test Apps API

```python
import pytest
import requests

def test_apps_api():
    """Test the apps API endpoint"""
    response = requests.get("http://localhost:8000/admin/api/v1/apps/")

    assert response.status_code == 200
    apps = response.json()

    # Check that apps is a list
    assert isinstance(apps, list)

    # Check app structure
    for app in apps:
        assert 'name' in app
        assert 'label' in app
        assert 'models' in app
        assert isinstance(app['models'], list)

        # Check model structure
        for model in app['models']:
            assert 'name' in model
            assert 'label' in model
            assert 'url' in model

def test_auth_app_exists():
    """Test that auth app is available"""
    response = requests.get("http://localhost:8000/admin/api/v1/apps/")
    apps = response.json()

    auth_app = next((app for app in apps if app['name'] == 'auth'), None)
    assert auth_app is not None
    assert auth_app['label'] == "Authentication & Authorization"
```

## Configuration

### API Version

The Apps API version is configured in your settings:

```python
# settings.py
ADMIN_PATH = "/admin"
API_VERSION = "v1"
```

### Custom App Configuration

```python
# apps.py
from fp_admin.admin.apps import AppConfig

class CustomAppConfig(AppConfig):
    name = "custom_app"
    verbose_name = "Custom Application"

    # Optional: Custom app-specific settings
    custom_setting = "value"
```

## Security

### Authentication

The Apps API may require authentication depending on your configuration:

```python
import requests

# With authentication
headers = {
    "Authorization": "Bearer your-token-here"
}
response = requests.get("http://localhost:8000/admin/api/v1/apps/", headers=headers)
```

### Rate Limiting

Consider implementing rate limiting for the Apps API:

```python
# Example rate limiting configuration
RATE_LIMIT = {
    "apps_api": {
        "requests_per_minute": 60,
        "burst": 10
    }
}
```

## Monitoring

### Health Checks

Monitor the Apps API health:

```python
def check_apps_api_health():
    """Check if the apps API is healthy"""
    try:
        response = requests.get("http://localhost:8000/admin/api/v1/apps/", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
```

### Metrics

Track API usage:

```python
import time

def track_apps_api_usage():
    """Track apps API response time and success rate"""
    start_time = time.time()

    try:
        response = requests.get("http://localhost:8000/admin/api/v1/apps/")
        response_time = time.time() - start_time

        # Log metrics
        print(f"APPS API RESPONSE TIME: {response_time:.3f}s")
        print(f"APPS API STATUS: {response.status_code}")

        return response.status_code == 200
    except Exception as e:
        print(f"APPS API ERROR: {e}")
        return False
```

## Next Steps

- **[Models API](models.md)** - Learn about the Models API for data operations
- **[Views API](views.md)** - Discover the Views API for UI configuration
- **[Authentication](../user-guide/authentication.md)** - Set up authentication for API access
- **[CLI Commands](../user-guide/cli-commands.md)** - Use CLI tools for development
