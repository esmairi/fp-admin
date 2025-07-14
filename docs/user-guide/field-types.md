# Field Types and Widgets Documentation

## Field Types and Widgets

fp-admin uses `FieldFactory` to create field configurations. Here are the available field types and their usage:

| **Field Type**  | **Factory Method**                | **Description**                                                    |
|-----------------|-----------------------------------|--------------------------------------------------------------------|
| `primarykey`    | `FieldFactory.primarykey_field()` | Primary key field (auto-increment, UUID, etc.) - always readonly  |
| `string`        | `FieldFactory.string_field()`     | Short or long text input                                          |
| `email`         | `FieldFactory.email_field()`      | Email input with validation                                       |
| `password`      | `FieldFactory.password_field()`   | Password input with hidden characters                             |
| `boolean`       | `FieldFactory.boolean_field()`    | True/false toggle                                                 |
| `textarea`      | `FieldFactory.textarea_field()`   | Multi-line text input                                             |
| `many_to_many`  | `FieldFactory.many_to_many_field()` | Many-to-many relationships                                       |
| `foreign_key`   | `FieldFactory.foreign_key_field()` | Foreign key relationships                                         |

## Field Factory Methods

### Primary Key Field

```python
FieldFactory.primarykey_field("id", "ID")
```

**Purpose**: Primary key field (readonly)
**Parameters**:
- `field_name`: The field name in the model
- `field_title`: Display title for the field

### String Field

```python
FieldFactory.string_field("username", "Username", required=True, min_length=3, max_length=150)
```

**Purpose**: Text input fields
**Parameters**:
- `field_name`: The field name in the model
- `field_title`: Display title for the field
- `required`: Whether the field is required (default: False)
- `min_length`: Minimum character length
- `max_length`: Maximum character length
- `pattern`: Regex pattern for validation

### Email Field

```python
FieldFactory.email_field("email", "Email", required=True)
```

**Purpose**: Email input with validation
**Parameters**:
- `field_name`: The field name in the model
- `field_title`: Display title for the field
- `required`: Whether the field is required (default: False)

### Password Field

```python
FieldFactory.password_field("password", "Password", required=True, min_length=8)
```

**Purpose**: Password input with hidden characters
**Parameters**:
- `field_name`: The field name in the model
- `field_title`: Display title for the field
- `required`: Whether the field is required (default: False)
- `min_length`: Minimum password length

### Boolean Field

```python
FieldFactory.boolean_field("is_active", "Active")
```

**Purpose**: True/false toggle
**Parameters**:
- `field_name`: The field name in the model
- `field_title`: Display title for the field

### Textarea Field

```python
FieldFactory.textarea_field("description", "Description", rows=5, max_length=200)
```

**Purpose**: Multi-line text input
**Parameters**:
- `field_name`: The field name in the model
- `field_title`: Display title for the field
- `rows`: Number of visible rows
- `max_length`: Maximum character length

### Many-to-Many Field

```python
FieldFactory.many_to_many_field(
    "groups",
    "Groups",
    model_class=Group,
    field_title="name"
)
```

**Purpose**: Many-to-many relationships
**Parameters**:
- `field_name`: The field name in the model
- `field_title`: Display title for the field
- `model_class`: The related model class
- `field_title`: The field to display from the related model

### Foreign Key Field

```python
FieldFactory.foreign_key_field(
    "category_id",
    "Category",
    model_class=Category,
    field_title="name"
)
```

**Purpose**: Foreign key relationships
**Parameters**:
- `field_name`: The field name in the model
- `field_title`: Display title for the field
- `model_class`: The related model class
- `field_title`: The field to display from the related model

## Field Configuration Examples

### Basic Form Fields

```python
from fp_admin.admin.fields import FieldFactory
from .models import User, Group, Permission

class UserFormView(BaseViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        # Primary key (readonly)
        FieldFactory.primarykey_field("id", "ID"),

        # String fields
        FieldFactory.string_field("username", "Username", required=True, min_length=3),
        FieldFactory.string_field("first_name", "First Name", required=True),
        FieldFactory.string_field("last_name", "Last Name", required=True),

        # Email field
        FieldFactory.email_field("email", "Email", required=True),

        # Password field
        FieldFactory.password_field("password", "Password", required=True, min_length=8),

        # Boolean fields
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),

        # Textarea field
        FieldFactory.textarea_field("bio", "Biography", rows=4, max_length=500),

        # Many-to-many relationships
        FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name"),
    ]
```

### List View Fields

```python
class UserListView(BaseViewBuilder):
    model = User
    view_type = "list"
    name = "UserList"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("username", "Username"),
        FieldFactory.string_field("first_name", "First Name"),
        FieldFactory.string_field("last_name", "Last Name"),
        FieldFactory.email_field("email", "Email"),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),
    ]
```

### Group Form Fields

```python
class GroupFormView(BaseViewBuilder):
    model = Group
    view_type = "form"
    name = "GroupForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("name", "Name", required=True, min_length=1),
        FieldFactory.string_field("description", "Description", required=True, min_length=1, max_length=200),
        FieldFactory.many_to_many_field("permissions", "Permissions", model_class=Permission, field_title="name"),
        FieldFactory.many_to_many_field("users", "Users", model_class=User, field_title="username"),
    ]
```

### Permission Form Fields

```python
class PermissionFormView(BaseViewBuilder):
    model = Permission
    view_type = "form"
    name = "PermissionForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("codename", "Code Name", required=True, min_length=1, max_length=150),
        FieldFactory.string_field("name", "Name", required=True, min_length=1, max_length=150),
        FieldFactory.string_field("description", "Description", required=True, min_length=1, max_length=200),
        FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name"),
    ]
```

## Field Validation

### String Validation

```python
# Required field with length constraints
FieldFactory.string_field(
    "title",
    "Title",
    required=True,
    min_length=1,
    max_length=200
)

# Field with pattern validation
FieldFactory.string_field(
    "phone",
    "Phone Number",
    pattern=r"^\+?1?\d{9,15}$"
)
```

### Email Validation

```python
# Email field with built-in validation
FieldFactory.email_field("email", "Email", required=True)
```

### Password Validation

```python
# Password with strength requirements
FieldFactory.password_field(
    "password",
    "Password",
    required=True,
    min_length=8
)
```

### Textarea Validation

```python
# Textarea with size constraints
FieldFactory.textarea_field(
    "description",
    "Description",
    rows=5,
    max_length=1000
)
```

## Relationship Fields

### Many-to-Many Relationships

```python
# User groups
FieldFactory.many_to_many_field(
    "groups",
    "Groups",
    model_class=Group,
    field_title="name"
)

# Group permissions
FieldFactory.many_to_many_field(
    "permissions",
    "Permissions",
    model_class=Permission,
    field_title="name"
)

# Group users
FieldFactory.many_to_many_field(
    "users",
    "Users",
    model_class=User,
    field_title="username"
)
```

### Foreign Key Relationships

```python
# User's department
FieldFactory.foreign_key_field(
    "department_id",
    "Department",
    model_class=Department,
    field_title="name"
)

# Post's author
FieldFactory.foreign_key_field(
    "author_id",
    "Author",
    model_class=User,
    field_title="username"
)
```

## Field Configuration Best Practices

### 1. Use Appropriate Field Types

```python
# Good: Use email field for email addresses
FieldFactory.email_field("email", "Email", required=True)

# Good: Use password field for passwords
FieldFactory.password_field("password", "Password", required=True, min_length=8)

# Good: Use boolean field for true/false values
FieldFactory.boolean_field("is_active", "Active")
```

### 2. Provide Meaningful Validation

```python
# String field with length validation
FieldFactory.string_field(
    "username",
    "Username",
    required=True,
    min_length=3,
    max_length=50
)

# Textarea with size limits
FieldFactory.textarea_field(
    "description",
    "Description",
    rows=4,
    max_length=500
)
```

### 3. Use Relationships Appropriately

```python
# Many-to-many for multiple selections
FieldFactory.many_to_many_field(
    "groups",
    "Groups",
    model_class=Group,
    field_title="name"
)

# Foreign key for single selection
FieldFactory.foreign_key_field(
    "category_id",
    "Category",
    model_class=Category,
    field_title="name"
)
```

### 4. Organize Fields Logically

```python
fields = [
    # Primary key first
    FieldFactory.primarykey_field("id", "ID"),

    # Basic information
    FieldFactory.string_field("username", "Username", required=True),
    FieldFactory.string_field("first_name", "First Name", required=True),
    FieldFactory.string_field("last_name", "Last Name", required=True),
    FieldFactory.email_field("email", "Email", required=True),

    # Security
    FieldFactory.password_field("password", "Password", required=True, min_length=8),
    FieldFactory.boolean_field("is_active", "Active"),
    FieldFactory.boolean_field("is_superuser", "Superuser"),

    # Relationships
    FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name"),
]
```

## Complete Example

Here's a complete example showing all field types in use:

```python
from fp_admin.admin.views import BaseViewBuilder
from fp_admin.admin.fields import FieldFactory
from .models import User, Group, Permission, Department

class UserFormView(BaseViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        # Primary key
        FieldFactory.primarykey_field("id", "ID"),

        # Basic information
        FieldFactory.string_field("username", "Username", required=True, min_length=3, max_length=150),
        FieldFactory.string_field("first_name", "First Name", required=True, max_length=100),
        FieldFactory.string_field("last_name", "Last Name", required=True, max_length=100),
        FieldFactory.email_field("email", "Email", required=True),

        # Security
        FieldFactory.password_field("password", "Password", required=True, min_length=8),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),

        # Additional information
        FieldFactory.textarea_field("bio", "Biography", rows=4, max_length=500),

        # Relationships
        FieldFactory.foreign_key_field("department_id", "Department", model_class=Department, field_title="name"),
        FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name"),
    ]

    creation_fields = ["username", "first_name", "last_name", "email", "password", "is_active", "is_superuser", "department_id"]
    allowed_update_fields = ["first_name", "last_name", "email", "is_active", "is_superuser", "bio", "department_id", "groups"]
```

This example demonstrates:
- All available field types
- Proper validation rules
- Relationship handling
- Field organization
- Creation and update field restrictions
