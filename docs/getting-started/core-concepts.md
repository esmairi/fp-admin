# Core Concepts

This guide explains the fundamental concepts behind fp-admin and how they work together.

## Overview

fp-admin is built around several core concepts that work together to provide a powerful admin interface:

- **Models**: SQLModel-based data models
- **Views**: Admin interface configurations
- **Fields**: Form field definitions and widgets
- **Apps**: Modular application organization
- **Services**: Business logic and CRUD operations

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

## Views

Views define how your models appear in the admin interface:

```python
from fp_admin.admin.views import AdminView
from fp_admin.admin.fields import FieldView

class UserView(AdminView):
    model = User
    label = "Users"
    list_fields = ["id", "username", "email", "is_active", "created_at"]
    search_fields = ["username", "email"]
    ordering_fields = ["username", "created_at"]

    def get_form_fields(self):
        return [
            FieldView.text_field("username", "Username", required=True),
            FieldView.email_field("email", "Email", required=True),
            FieldView.switch_field("is_active", "Active"),
        ]
```

### View Features

- **List Display**: Configure which fields appear in the list view
- **Search**: Define searchable fields
- **Ordering**: Specify sortable fields
- **Form Fields**: Define form field types and widgets
- **Permissions**: Control access to views
- **Custom Actions**: Add custom actions to views

## Fields

Fields define the form inputs and their behavior:

```python
from fp_admin.admin.fields import FieldView

# Basic text field
FieldView.text_field("name", "Name", required=True)

# Email field with validation
FieldView.email_field("email", "Email Address")

# Foreign key relationship
FieldView.foreign_key_field("category_id", "Category", model=Category)

# Multi-choice field
FieldView.multi_choice_field("tags", "Tags", choices=tag_choices)
```

### Field Types

- **string**: Text input (default)
- **number**: Numeric input
- **boolean**: True/false toggle
- **date**: Date picker
- **datetime**: Date and time picker
- **choice**: Single selection
- **multichoice**: Multiple selections
- **foreignkey**: Related model selection
- **many_to_many**: Many-to-many relationships
- **file**: File upload
- **image**: Image upload
- **json**: JSON editor

### Widgets

Each field type supports different widgets:

- **text**: Single-line text input
- **textarea**: Multi-line text input
- **password**: Password input
- **dropdown**: Select dropdown
- **radio**: Radio buttons
- **checkbox**: Checkbox
- **switch**: Toggle switch
- **slider**: Numeric slider
- **calendar**: Date/time picker
- **upload**: File upload
- **image**: Image upload with preview
- **editor**: Code/JSON editor
- **colorPicker**: Color picker

## Apps

Apps are modular components that organize your code:

```python
# apps/blog/apps.py
from fp_admin.apps import AppConfig

class BlogConfig(AppConfig):
    name = "blog"
    label = "blog"
    views = [
        "apps.blog.views.PostView",
        "apps.blog.views.CategoryView",
    ]
```

### App Structure

```
apps/
├── blog/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── routers.py
│   └── views.py
└── auth/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── routers.py
    └── views.py
```

### App Features

- **Modular Design**: Each app is self-contained
- **Reusable**: Apps can be shared between projects
- **Configurable**: Apps can be enabled/disabled
- **Extensible**: Apps can be extended with custom functionality

## Services

Services handle business logic and CRUD operations:

```python
from fp_admin.services import ModelService

class UserService(ModelService):
    model = User

    def create_user(self, data):
        # Custom business logic
        user = User(**data)
        # Additional processing
        return user
```

### Service Features

- **CRUD Operations**: Automatic create, read, update, delete
- **Validation**: Built-in data validation
- **Error Handling**: Comprehensive error handling
- **Custom Logic**: Extensible with custom business logic
- **Query Building**: Advanced query building with filters

## FieldView System

The FieldView system is the core of fp-admin's flexibility:

```python
from fp_admin.admin.fields import FieldView, FieldFactory

# Using FieldView directly
field = FieldView(
    name="title",
    label="Title",
    field_type="string",
    widget="text",
    required=True
)

# Using FieldFactory for convenience
field = FieldFactory.text_field("title", "Title", required=True)
field = FieldFactory.email_field("email", "Email")
field = FieldFactory.switch_field("is_active", "Active")
```

### FieldView Features

- **Type Safety**: Strong typing for field configurations
- **Validation**: Built-in validation rules
- **Widgets**: Rich widget support
- **Relationships**: Foreign key and many-to-many support
- **Customization**: Highly customizable appearance and behavior

## Admin Interface

The admin interface is automatically generated from your views:

### Features

- **Responsive Design**: Works on desktop and mobile
- **Modern UI**: Clean, modern interface
- **Search**: Full-text search across models
- **Filtering**: Advanced filtering options
- **Sorting**: Sort by any field
- **Pagination**: Efficient data pagination
- **Bulk Actions**: Perform actions on multiple items
- **Export**: Export data in various formats

### Navigation

- **Model List**: Browse all models
- **Detail Views**: View and edit individual records
- **Create Forms**: Add new records
- **Search**: Find specific records
- **Settings**: Configure admin interface

## API Layer

fp-admin provides a complete REST API:

### Endpoints

- `GET /api/v1/models/{model}/` - List records
- `POST /api/v1/models/{model}/` - Create record
- `GET /api/v1/models/{model}/{id}/` - Get record
- `PUT /api/v1/models/{model}/{id}/` - Update record
- `DELETE /api/v1/models/{model}/{id}/` - Delete record

### Features

- **Authentication**: JWT-based authentication
- **Authorization**: Role-based access control
- **Validation**: Request/response validation
- **Error Handling**: Comprehensive error responses
- **Documentation**: Auto-generated API documentation

## Database Integration

fp-admin uses SQLModel for database operations:

### Features

- **Multiple Databases**: Support for SQLite, PostgreSQL, MySQL
- **Migrations**: Alembic-based migration system
- **Relationships**: Foreign keys and many-to-many
- **Indexing**: Automatic index creation
- **Constraints**: Database-level constraints

### Migration System

```bash
# Create migration
fp-admin make-migrations

# Apply migrations
fp-admin migrate

# Rollback migration
fp-admin migrate --revision=previous
```

## Authentication & Authorization

fp-admin includes a complete authentication system:

### Features

- **User Management**: User creation and management
- **Role-based Access**: Control access by user roles
- **JWT Tokens**: Secure token-based authentication
- **Password Security**: Secure password hashing
- **Session Management**: Session handling

### User Model

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## CLI Tools

fp-admin provides command-line tools for development:

### Commands

- `fp-admin startproject` - Create new project
- `fp-admin startapp` - Create new app
- `fp-admin makemigrations` - Create database migrations
- `fp-admin migrate` - Apply migrations
- `fp-admin createsuperuser` - Create admin user
- `fp-admin run` - Start development server

## Configuration

fp-admin is highly configurable through settings:

```python
# settings.py
from fp_admin.global_settings import *

# Database
DATABASE_URL = "sqlite:///./app.db"

# Admin Settings
ADMIN_TITLE = "My Admin"
ADMIN_DESCRIPTION = "Admin interface"

# Security
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# File Upload
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024
```

## Next Steps

Now that you understand the core concepts, explore:

- **[Field Types](../user-guide/field-types.md)** - Detailed field type reference
- **[Widgets](../user-guide/widgets.md)** - Available widgets and configurations
- **[Admin Models](../user-guide/admin-models.md)** - Advanced admin configuration
- **[Authentication](../user-guide/authentication.md)** - User management setup
- **[CLI Commands](../user-guide/cli-commands.md)** - Command-line tools reference
