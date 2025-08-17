# Core Concepts

This guide explains the fundamental concepts behind fp-admin and how they work together.

## Overview

fp-admin is built around several core concepts that work together to provide a powerful admin interface:

- **Models**: SQLModel-based data models
- **Admin Registration**: Simple model registration in admin.py
- **Views**: Detailed admin interface configurations in views.py
- **Fields**: Form field definitions and widgets
- **Apps**: Modular application organization
- **Services**: Business logic and CRUD operations
- **Providers**: Authentication and external service integrations
- **Module Loader**: Automatic discovery and loading of application components

## Models

Models are the foundation of your application. They define your data structure using SQLModel:

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Model Features

- **Automatic CRUD**: Models automatically get create, read, update, delete operations
- **REST API**: Each model gets REST API endpoints
- **Admin Interface**: Models can be configured for admin interface display
- **Validation**: Built-in validation based on field types and constraints
- **Relationships**: Support for foreign keys and many-to-many relationships

## Admin Registration

Admin registration is the simple process of registering your models with the admin interface:

```python
from fp_admin.registry import AdminModel
from .models import User, Post, Category

class UserAdmin(AdminModel):
    model = User
    label = "Users"
    display_field = "username"  # Field to display in lists

class PostAdmin(AdminModel):
    model = Post
    label = "Posts"
    display_field = "title"

class CategoryAdmin(AdminModel):
    model = Category
    label = "Categories"
    display_field = "name"
```

### Admin Registration Features

- **Simple Setup**: Just specify the model and label
- **Automatic Discovery**: Models are automatically discovered by the admin interface
- **Clean Separation**: Keeps model registration separate from view configuration
- **Minimal Code**: Requires only the essential information
- **Display Fields**: Configure which field to show in list views

## Services Layer

The services layer provides business logic and CRUD operations for your models:

```python
from fp_admin.services.v1 import CreateService, ListService, ReadService, UpdateService

# Create service for User model
create_service = CreateService(User, "user")

# List service for paginated results
list_service = ListService(User, "user")

# Read service for single record operations
read_service = ReadService(User, "user")

# Update service for record modifications
update_service = UpdateService(User, "user")
```

### Service Features

- **CRUD Operations**: Complete create, read, update, delete functionality
- **Pagination**: Built-in pagination support
- **Filtering**: Advanced filtering and querying capabilities
- **Validation**: Form-based validation with custom error handling
- **Relationship Handling**: Automatic relationship field loading
- **Async Support**: Full async/await support for database operations

## Authentication & Providers

fp-admin includes a flexible authentication system with multiple provider support:

```python
from fp_admin.providers import InternalProvider
from fp_admin.providers.exceptions import AuthError

# Internal authentication provider
provider = InternalProvider(
    secret_key="your-secret-key",
    access_token_expires_minutes=30,
    refresh_token_expires_minutes=90,
    user_auth_func=your_auth_function
)

# Authenticate user and issue tokens
token_data = await provider.authenticate_and_issue_token(username, password)
```

### Authentication Features

- **JWT Tokens**: Secure access and refresh token system
- **Multiple Providers**: Support for internal and OAuth providers
- **Token Refresh**: Automatic token refresh mechanism
- **Secure Storage**: Argon2 password hashing
- **Session Management**: Flexible session handling

## Module Loading

The module loader automatically discovers and loads your application components:

```python
# Automatic loading order
module_order = ["models", "admin", "views", "apps"]

# Apps are loaded from INSTALLED_APPS setting
INSTALLED_APPS = [
    "fp_admin.apps.auth",
    "your_app.blog",
    "your_app.users"
]
```

### Module Loading Features

- **Automatic Discovery**: No manual imports required
- **Ordered Loading**: Ensures dependencies are loaded correctly
- **Router Registration**: Automatic API router registration
- **Error Handling**: Graceful handling of missing modules
- **Hot Reloading**: Support for development-time module reloading

## Views

Views define the detailed configuration of how your models appear in the admin interface:

```python
from fp_admin.registry import ViewBuilder
from fp_admin.models.field import FieldFactory
from .models import User # your models.py

class UserFormView(ViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"
    fields = [
        FieldFactory.primary_key_field("id"),
        FieldFactory.string_field(
            "username",
            required=True,
        ),
        FieldFactory.email_field("email", required=True),
        FieldFactory.boolean_field("is_active"),
        ...
    ]
    creation_fields = ["username", "email", "is_active"]
    allowed_update_fields = ["email", "is_active"]
```

### View Features

- **Field Configuration**: Detailed control over form fields
- **Validation Rules**: Custom validation and error messages
- **Permission Control**: Field-level access control
- **Widget Selection**: Choose appropriate input widgets
- **Relationship Display**: Handle foreign key and many-to-many fields

## Apps

Apps are modular components that group related functionality:

```python
# apps/blog/apps.py
from fp_admin.registry import AppConfig

class BlogApp(AppConfig):
    name = "blog"
    label = "Blog"
    description = "Blog management application"
    icon = "mdi-post"
    order = 1
```

### App Features

- **Modular Design**: Organize functionality into logical groups
- **Icon Support**: Visual representation in admin interface
- **Ordering**: Control display order in navigation
- **Dependencies**: Manage app dependencies and requirements
- **Configuration**: App-specific settings and options

## Registry System

The registry system manages all registered components:

```python
from fp_admin.registry import model_registry, view_registry, apps_registry

# Get registered model configuration
model_config = model_registry.get("user")

# Get registered view configuration
view_config = view_registry.get("UserForm")

# Get registered app configuration
app_config = apps_registry.get("blog")
```

### Registry Features

- **Central Management**: Single source of truth for all components
- **Type Safety**: Full type hints and validation
- **Configuration Access**: Easy access to component configurations
- **Dynamic Registration**: Runtime component registration
- **Validation**: Ensure component configurations are valid

## Error Handling

fp-admin provides comprehensive error handling and validation:

```python
from fp_admin.exceptions import ModelError, ServiceError, ValidationError
from fp_admin.api.error_handlers import handle_validation_error

try:
    result = await service.create_record(session, params)
except ValidationError as e:
    raise handle_validation_error(e.details)
except ServiceError as e:
    # Handle service-level errors
    pass
```

### Error Handling Features

- **Structured Errors**: Consistent error response format
- **Validation Errors**: Detailed field-level validation errors
- **HTTP Status Codes**: Appropriate HTTP status codes
- **Error Logging**: Comprehensive error logging
- **User-Friendly Messages**: Clear error messages for end users
