# Views API

This guide covers the REST API endpoints for admin view configuration in fp-admin.

## Overview

The Views API provides endpoints for retrieving admin view configurations, form schemas, and view metadata.

## Base URL

All view API endpoints are prefixed with `/api/v1/views/`:

```
https://your-domain.com/api/v1/views/
```

## Authentication

All API endpoints require authentication. Include the JWT token in the Authorization header:

```bash
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### List Views

**GET** `/api/v1/views/`

Retrieve a list of all available admin views.

#### Example Request

```bash
GET /api/v1/views/
```

#### Response Format

```json
{
  "count": 5,
  "results": [
    {
      "id": "user",
      "name": "UserView",
      "label": "Users",
      "model": "User",
      "app": "auth",
      "list_fields": ["id", "username", "email", "is_active"],
      "search_fields": ["username", "email"],
      "ordering_fields": ["username", "created_at"],
      "url": "/api/v1/views/user/"
    },
    {
      "id": "post",
      "name": "PostView",
      "label": "Blog Posts",
      "model": "Post",
      "app": "blog",
      "list_fields": ["id", "title", "author", "published"],
      "search_fields": ["title", "content"],
      "ordering_fields": ["title", "created_at"],
      "url": "/api/v1/views/post/"
    }
  ]
}
```

### Get View Details

**GET** `/api/v1/views/{model_name}/`

Retrieve detailed information about a specific admin view.

#### Example Request

```bash
GET /api/v1/views/user/
```

#### Response Format

```json
{
  "id": "user",
  "name": "UserView",
  "label": "Users",
  "model": "User",
  "app": "auth",
  "list_fields": ["id", "username", "email", "is_active", "created_at"],
  "search_fields": ["username", "email"],
  "ordering_fields": ["username", "email", "created_at"],
  "readonly_fields": ["created_at", "updated_at"],
  "exclude_fields": ["password"],
  "list_per_page": 20,
  "list_max_show_all": 1000,
  "date_hierarchy": "created_at",
  "empty_value_display": "-",
  "form_fields": [
    {
      "name": "username",
      "label": "Username",
      "field_type": "string",
      "widget": "text",
      "required": true,
      "max_length": 150,
      "help_text": "Required. 150 characters or fewer."
    },
    {
      "name": "email",
      "label": "Email",
      "field_type": "string",
      "widget": "email",
      "required": true,
      "help_text": "Required. Enter a valid email address."
    },
    {
      "name": "is_active",
      "label": "Active",
      "field_type": "boolean",
      "widget": "switch",
      "required": false,
      "default": true,
      "help_text": "Designates whether this user should be treated as active."
    }
  ],
  "actions": [
    {
      "name": "activate_selected",
      "label": "Activate selected users",
      "description": "Activate the selected users"
    },
    {
      "name": "deactivate_selected",
      "label": "Deactivate selected users",
      "description": "Deactivate the selected users"
    }
  ],
  "filters": [
    {
      "name": "is_active",
      "label": "Active",
      "field": "is_active",
      "type": "boolean"
    },
    {
      "name": "created_date",
      "label": "Created date",
      "field": "created_at",
      "type": "date"
    }
  ]
}
```

### Get Form Schema (TODO)

**GET** `/api/v1/views/{model_name}/form/`

Retrieve the form schema for creating/editing records in this view.

#### Example Request

```bash
GET /api/v1/views/user/form/
```

#### Response Format

```json
{
  "title": "Add User",
  "method": "POST",
  "action": "/api/v1/models/user/",
  "fields": [
    {
      "name": "username",
      "label": "Username",
      "type": "string",
      "widget": "text",
      "required": true,
      "max_length": 150,
      "help_text": "Required. 150 characters or fewer.",
      "placeholder": "Enter username",
      "validation": {
        "pattern": "^[a-zA-Z0-9_]+$",
        "message": "Username can only contain letters, numbers, and underscores."
      }
    },
    {
      "name": "email",
      "label": "Email",
      "type": "string",
      "widget": "email",
      "required": true,
      "help_text": "Required. Enter a valid email address.",
      "placeholder": "Enter email address",
      "validation": {
        "pattern": "^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$",
        "message": "Enter a valid email address."
      }
    },
    {
      "name": "password",
      "label": "Password",
      "type": "string",
      "widget": "password",
      "required": true,
      "help_text": "Enter a secure password.",
      "validation": {
        "min_length": 8,
        "pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]",
        "message": "Password must be at least 8 characters and contain uppercase, lowercase, digit, and special character."
      }
    },
    {
      "name": "is_active",
      "label": "Active",
      "type": "boolean",
      "widget": "switch",
      "required": false,
      "default": true,
      "help_text": "Designates whether this user should be treated as active."
    }
  ],
  "validation": {
    "username": {
      "unique": true,
      "message": "A user with that username already exists."
    },
    "email": {
      "unique": true,
      "message": "A user with that email already exists."
    }
  }
}
```

### Get Edit Form Schema (TODO)

**GET** `/api/v1/views/{view_id}/form/{id}/`

Retrieve the form schema for editing a specific record.

#### Example Request

```bash
GET /api/v1/views/user/form/1/
```

#### Response Format

```json
{
  "title": "Change User",
  "method": "PUT",
  "action": "/api/v1/models/user/1/",
  "fields": [
    {
      "name": "username",
      "label": "Username",
      "type": "string",
      "widget": "text",
      "required": true,
      "value": "john_doe",
      "max_length": 150,
      "help_text": "Required. 150 characters or fewer.",
      "readonly": false
    },
    {
      "name": "email",
      "label": "Email",
      "type": "string",
      "widget": "email",
      "required": true,
      "value": "john@example.com",
      "help_text": "Required. Enter a valid email address.",
      "readonly": false
    },
    {
      "name": "is_active",
      "label": "Active",
      "type": "boolean",
      "widget": "switch",
      "required": false,
      "value": true,
      "help_text": "Designates whether this user should be treated as active.",
      "readonly": false
    },
    {
      "name": "created_at",
      "label": "Created at",
      "type": "datetime",
      "widget": "datetime",
      "required": false,
      "value": "2023-01-01T00:00:00Z",
      "help_text": "Date and time when this user was created.",
      "readonly": true
    }
  ],
  "validation": {
    "username": {
      "unique": true,
      "exclude": 1,
      "message": "A user with that username already exists."
    },
    "email": {
      "unique": true,
      "exclude": 1,
      "message": "A user with that email already exists."
    }
  }
}
```

### Get View Actions (TODO)

**GET** `/api/v1/views/{view_id}/actions/`

Retrieve available actions for a specific view.

#### Example Request

```bash
GET /api/v1/views/user/actions/
```

#### Response Format

```json
{
  "actions": [
    {
      "name": "activate_selected",
      "label": "Activate selected users",
      "description": "Activate the selected users",
      "icon": "check_circle",
      "confirmation": "Are you sure you want to activate the selected users?",
      "permission": "auth.change_user"
    },
    {
      "name": "deactivate_selected",
      "label": "Deactivate selected users",
      "description": "Deactivate the selected users",
      "icon": "cancel",
      "confirmation": "Are you sure you want to deactivate the selected users?",
      "permission": "auth.change_user"
    },
    {
      "name": "delete_selected",
      "label": "Delete selected users",
      "description": "Delete the selected users",
      "icon": "delete",
      "confirmation": "Are you sure you want to delete the selected users? This action cannot be undone.",
      "permission": "auth.delete_user"
    }
  ]
}
```




### Get View Permissions (TODO)

**GET** `/api/v1/views/{view_id}/permissions/`

Retrieve permissions required for this view.

#### Example Request

```bash
GET /api/v1/views/user/permissions/
```

#### Response Format

```json
{
  "permissions": {
    "view": "auth.view_user",
    "add": "auth.add_user",
    "change": "auth.change_user",
    "delete": "auth.delete_user"
  },
  "user_permissions": {
    "view": true,
    "add": true,
    "change": false,
    "delete": false
  }
}
```

## Field Types

### String Fields

```json
{
  "name": "username",
  "label": "Username",
  "type": "string",
  "widget": "text",
  "required": true,
  "max_length": 150,
  "min_length": 3,
  "pattern": "^[a-zA-Z0-9_]+$",
  "placeholder": "Enter username",
  "help_text": "Required. 150 characters or fewer."
}
```

### Number Fields

```json
{
  "name": "age",
  "label": "Age",
  "type": "number",
  "widget": "number",
  "required": false,
  "min_value": 0,
  "max_value": 120,
  "step": 1,
  "help_text": "Enter age in years."
}
```

### Boolean Fields

```json
{
  "name": "is_active",
  "label": "Active",
  "type": "boolean",
  "widget": "switch",
  "required": false,
  "default": true,
  "help_text": "Designates whether this user should be treated as active."
}
```

### Date/Time Fields

```json
{
  "name": "birth_date",
  "label": "Birth Date",
  "type": "date",
  "widget": "date",
  "required": false,
  "format": "YYYY-MM-DD",
  "min_date": "1900-01-01",
  "max_date": "2023-12-31",
  "help_text": "Enter birth date."
}
```

### Choice Fields

```json
{
  "name": "status",
  "label": "Status",
  "type": "choice",
  "widget": "select",
  "required": true,
  "choices": [
    {"value": "draft", "label": "Draft"},
    {"value": "published", "label": "Published"},
    {"value": "archived", "label": "Archived"}
  ],
  "default": "draft",
  "help_text": "Select the status of this item."
}
```

### Foreign Key Fields

```json
{
  "name": "category_id",
  "label": "Category",
  "type": "foreign_key",
  "widget": "select",
  "required": false,
  "model": "Category",
  "display_field": "name",
  "searchable": true,
  "help_text": "Select a category for this item."
}
```

### Many-to-Many Fields

```json
{
  "name": "tags",
  "label": "Tags",
  "type": "many_to_many",
  "widget": "multi_select",
  "required": false,
  "model": "Tag",
  "display_field": "name",
  "max_selections": 5,
  "help_text": "Select up to 5 tags for this item."
}
```

## Widget Types

### Text Inputs

- `text`: Single-line text input
- `textarea`: Multi-line text input
- `password`: Password input
- `email`: Email input
- `url`: URL input

### Number Inputs

- `number`: Number input
- `slider`: Slider for numeric values
- `range`: Range slider

### Date/Time Inputs

- `date`: Date picker
- `time`: Time picker
- `datetime`: Date and time picker

### Boolean Inputs

- `checkbox`: Checkbox
- `switch`: Toggle switch
- `radio`: Radio buttons

### Choice Inputs

- `select`: Dropdown select
- `radio`: Radio buttons
- `buttons`: Button group

### Multi-Choice Inputs

- `multi_select`: Multi-select dropdown
- `chips`: Chip-style multi-select
- `list_box`: List box

### File Inputs

- `file`: File upload
- `image`: Image upload with preview

### Advanced Inputs

- `rich_text`: Rich text editor
- `markdown`: Markdown editor
- `json`: JSON editor
- `color`: Color picker

## Error Handling

### Validation Errors

```json
{
  "detail": "Form validation failed",
  "errors": {
    "username": [
      "This field is required."
    ],
    "email": [
      "Enter a valid email address."
    ],
    "password": [
      "Password must be at least 8 characters long."
    ]
  }
}
```

### Permission Errors

```json
{
  "detail": "You do not have permission to access this view."
}
```

### Not Found Errors

```json
{
  "detail": "View not found"
}
```

## Examples

### User Management View

```bash
# Get user view details
GET /api/v1/views/user/

# Get user form schema
GET /api/v1/views/user/form/

# Get user edit form
GET /api/v1/views/user/form/1/

# Get user actions
GET /api/v1/views/user/actions/

# Get user filters
GET /api/v1/views/user/filters/
```

### Blog Post View

```bash
# Get post view details
GET /api/v1/views/post/

# Get post form schema
GET /api/v1/views/post/form/

# Get post edit form
GET /api/v1/views/post/form/1/

# Get post actions
GET /api/v1/views/post/actions/
```

## Next Steps

- **[Models API](models.md)** - REST API for model CRUD operations
- **[Apps API](apps.md)** - Application management API
- **[Admin Models](../user-guide/admin-models.md)** - Configure admin interfaces
