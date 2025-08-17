# Admin Models

Admin models define how your SQLModel classes appear in the fp-admin interface. They provide a simple way to register models and configure their display in the admin panel.

## Overview

Admin models use the `AdminModel` class to register your models with the admin interface. This is separate from view configuration and provides basic model registration with minimal configuration.

## Basic Admin Model Registration

### Simple Registration

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

### Admin Model Features

- **Simple Setup**: Just specify the model and label
- **Automatic Discovery**: Models are automatically discovered by the admin interface
- **Clean Separation**: Keeps model registration separate from view configuration
- **Minimal Code**: Requires only the essential information
- **Display Fields**: Configure which field to show in list views

## Admin Model Configuration

### Required Attributes

```python
class UserAdmin(AdminModel):
    model = User          # Required: Your SQLModel class
    label = "Users"       # Required: Display name in admin
    display_field = "username"  # Required: Field to show in lists
```

### Optional Attributes

```python
class UserAdmin(AdminModel):
    model = User
    label = "Users"
    display_field = "username"

    # Optional: Custom ordering
    ordering = ["username"]

    # Optional: Fields to include in list view
    list_fields = ["id", "username", "email", "is_active"]

    # Optional: Fields to exclude from list view
    exclude_fields = ["password_hash", "created_at", "updated_at"]
```

## View Configuration (views.py)

Views define the detailed configuration of how your models appear in the admin interface using `ViewBuilder`:

```python
from fp_admin.registry import ViewBuilder
from fp_admin.models.field import FieldFactory
from .models import User, Group, Permission

class UserFormView(ViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"
    fields = [
        FieldFactory.primary_key_field("id"),
        FieldFactory.string_field("username", required=True, min_length=3),
        FieldFactory.string_field("first_name", required=True),
        FieldFactory.string_field("last_name", required=True),
        FieldFactory.email_field("email", required=True),
        FieldFactory.password_field("password", required=True, min_length=8),
        FieldFactory.boolean_field("is_active", required=True),
        FieldFactory.boolean_field("is_superuser", required=True),
        FieldFactory.foreignkey_field(
            "group_id",
            model_class=Group,
            display_field="name",
            required=False
        ),
    ]
    creation_fields = ["username", "first_name", "last_name", "email", "password", "is_active", "is_superuser"]
    allowed_update_fields = ["first_name", "last_name", "email", "is_active", "is_superuser", "group_id"]
```

### View Features

- **Field Configuration**: Detailed control over form fields
- **Validation Rules**: Custom validation and error messages
- **Permission Control**: Field-level access control
- **Widget Selection**: Choose appropriate input widgets
- **Relationship Display**: Handle foreign key and many-to-many fields

## Complete Example

Here's a complete example based on the auth app:

```python
from fp_admin.registry import AdminModel, ViewBuilder
from fp_admin.models.field import FieldFactory
from .models import User, Group, Permission

# Admin Model Registration
class UserAdmin(AdminModel):
    model = User
    label = "Users"
    display_field = "username"

class GroupAdmin(AdminModel):
    model = Group
    label = "Groups"
    display_field = "name"

class PermissionAdmin(AdminModel):
    model = Permission
    label = "Permissions"
    display_field = "name"

# User Form View
class UserFormView(ViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        FieldFactory.primary_key_field("id"),
        FieldFactory.string_field("username", required=True, min_length=3),
        FieldFactory.email_field("email", required=True),
        FieldFactory.password_field("password", required=True, min_length=8),
        FieldFactory.boolean_field("is_active", required=True),
        FieldFactory.boolean_field("is_superuser", required=True),
        FieldFactory.many_to_many_field("groups", model_class=Group, display_field="name"),
    ]

    creation_fields = ["username", "email", "password", "is_active", "is_superuser"]
    allowed_update_fields = ["email", "is_active", "is_superuser"]

# User List View
class UserListView(ViewBuilder):
    model = User
    view_type = "list"
    name = "UserList"

    fields = [
        FieldFactory.primary_key_field("id"),
        FieldFactory.string_field("username"),
        FieldFactory.email_field("email"),
        FieldFactory.boolean_field("is_active"),
        FieldFactory.boolean_field("is_superuser"),
    ]

# Group Form View
class GroupFormView(ViewBuilder):
    model = Group
    view_type = "form"
    name = "GroupForm"

    fields = [
        FieldFactory.primary_key_field("id"),
        FieldFactory.string_field("name", required=True, min_length=1),
        FieldFactory.string_field("description", required=True, min_length=1, max_length=200),
        FieldFactory.many_to_many_field("permissions", model_class=Permission, display_field="name"),
        FieldFactory.many_to_many_field("users", model_class=User, display_field="username"),
    ]

    creation_fields = ["name", "description"]
    allowed_update_fields = ["name", "description", "permissions"]
```

## Field Configuration Options

### String Fields

```python
# String field with validation
FieldFactory.string_field(
    "title",
    required=True,
    min_length=1,
    max_length=200
)

# Email field with pattern validation
FieldFactory.email_field(
    "email",
    required=True
)

# Password field with strength requirements
FieldFactory.password_field(
    "password",
    required=True,
    min_length=8
)
```

### Numeric Fields

```python
# Number field with range validation
FieldFactory.number_field(
    "age",
    required=True,
    min_value=13,
    max_value=120
)

# Float field with precision
FieldFactory.float_field(
    "price",
    required=True,
    min_value=0.0,
    step=0.01
)
```

### Boolean Fields

```python
# Standard boolean field
FieldFactory.boolean_field("is_active", required=True)

# Toggle field (switch widget)
FieldFactory.toggle_field("is_verified", required=True)

# Radio field for multiple options
FieldFactory.radio_field("status", choices=["active", "inactive", "pending"])
```

### Choice Fields

```python
# Single choice field
FieldFactory.choice_field("category", required=True, choices=["tech", "lifestyle", "news"])

# Multiple choice field
FieldFactory.multichoice_field("tags", required=True, choices=["python", "fastapi", "admin"])

# Chips field for multiple selections
FieldFactory.chips_field("skills", required=True, choices=["python", "javascript", "sql"])
```

### Relationship Fields

```python
# Foreign key field
FieldFactory.foreignkey_field(
    "category_id",
    model_class=Category,
    display_field="name",
    required=True
)

# Many-to-many field
FieldFactory.many_to_many_field(
    "tags",
    model_class=Tag,
    display_field="name",
    required=False
)

# One-to-one field
FieldFactory.one_to_one_field(
    "profile",
    model_class=UserProfile,
    display_field="username",
    required=False
)
```

### File Fields

```python
# File upload field
FieldFactory.file_field("document", required=True)

# Image field with preview
FieldFactory.image_field("avatar", required=True)
```

### Special Fields

```python
# JSON field
FieldFactory.json_field("metadata", required=True)

# Autocomplete field
FieldFactory.autocomplete_field("search", required=True, placeholder="Start typing...")
```

## Best Practices

1. **Use descriptive names**: Choose clear, descriptive names for your views
2. **Separate concerns**: Use different views for different operations (form vs list)
3. **Validate fields**: Always specify required fields and validation rules
4. **Control updates**: Use `allowed_update_fields` to restrict what can be changed
5. **Use relationships**: Leverage `many_to_many_field` and `foreignkey_field` for relationships
6. **Follow naming conventions**: Use consistent naming patterns across your views

## Field Validation

### Built-in Validation

Each field type includes appropriate validation:

- **String fields**: Length constraints, pattern matching
- **Email fields**: Email format validation
- **Numeric fields**: Range validation, type checking
- **Date fields**: Date format validation
- **Required fields**: Non-empty value validation

### Custom Validation

You can add custom validation to any field:

```python
from fp_admin.models.field import FpFieldValidator, FpFieldError

# Custom validator
def validate_username_unique(value: str) -> FpFieldError | None:
    if value == "admin":
        return FpFieldError(
            code="reserved_username",
            message="Username 'admin' is reserved"
        )
    return None

# Apply custom validator
FieldFactory.string_field(
    "username",
    required=True,
    custom_validator=validate_username_unique
)
```

## Performance Optimization

### Field Selection

Only include fields that are necessary for your use case:

```python
# Minimal fields for list view
list_fields = [
    FieldFactory.primary_key_field("id"),
    FieldFactory.string_field("username"),
    FieldFactory.email_field("email"),
    FieldFactory.boolean_field("is_active"),
]

# Full fields for form view
form_fields = [
    # ... all fields including relationships
]
```

### Relationship Loading

Configure relationship fields with appropriate display fields:

```python
# Efficient relationship field
FieldFactory.many_to_many_field(
    "groups",
    model_class=Group,
    display_field="name",  # Only load the name field
    required=False
)
```

## Testing Admin Models

### Unit Testing

```python
import pytest
from fp_admin.registry import AdminModel, ViewBuilder
from fp_admin.models.field import FieldFactory

def test_user_admin_model():
    """Test user admin model configuration."""
    admin = UserAdmin()

    assert admin.model == User
    assert admin.label == "Users"
    assert admin.display_field == "username"

def test_user_form_view():
    """Test user form view configuration."""
    view = UserFormView()

    assert view.model == User
    assert view.view_type == "form"
    assert len(view.fields) > 0

    # Check required fields
    username_field = next(f for f in view.fields if f.name == "username")
    assert username_field.required is True
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_admin_model_registration():
    """Test that admin models are properly registered."""
    from fp_admin.registry import model_registry

    # Check if user model is registered
    user_config = model_registry.get("user")
    assert user_config is not None
    assert user_config.model == User
    assert user_config.label == "Users"
```

## Next Steps

- **[Field Types](../user-guide/field-types.md)** - Learn about all available field types
- **[Widgets](../user-guide/widgets.md)** - Discover available widgets and their configuration
- **[Services Layer](../user-guide/services.md)** - Learn about the services architecture
- **[API Reference](../api/models.md)** - Explore the REST API endpoints
