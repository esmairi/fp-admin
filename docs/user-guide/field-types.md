# Field Types

fp-admin provides a comprehensive set of field types through the `FieldFactory` class. Each field type is designed to handle specific data types and provide appropriate validation and widgets.

## Overview

The `FieldFactory` class provides methods to create different types of fields for your admin forms and views. Each field type includes:

- **Type-specific validation**: Built-in validation for the field type
- **Widget selection**: Appropriate input widgets for the field type
- **Configuration options**: Flexible configuration through keyword arguments
- **Relationship support**: Special handling for foreign keys and many-to-many fields

## Basic Field Types

### Primary Key Fields

```python
from fp_admin.models.field import FieldFactory

# Primary key field (readonly)
FieldFactory.primary_key_field("id")
```

### Text Fields

```python
# String input field
FieldFactory.string_field("username", required=True, placeholder="Enter username")

# Text area field
FieldFactory.text_field("description", placeholder="Enter description")

# Email field with validation
FieldFactory.email_field("email", required=True, placeholder="Enter email")

# Password field
FieldFactory.password_field("password", required=True, placeholder="Enter password")
```

### Numeric Fields

```python
# Integer field
FieldFactory.number_field("age", required=True, placeholder="Enter age")

# Float field
FieldFactory.float_field("price", required=True, placeholder="Enter price")

# Slider field (same as number field)
FieldFactory.slider_field("rating", required=True)
```

### Date and Time Fields

```python
# Date field
FieldFactory.date_field("birth_date", required=True)

# Time field
FieldFactory.time_field("appointment_time", required=True)

# DateTime field
FieldFactory.datetime_field("created_at", required=True)
```

### Boolean Fields

```python
# Boolean field
FieldFactory.boolean_field("is_active", required=True)

# Toggle field (switch widget)
FieldFactory.toggle_field("is_verified", required=True)

# Radio field
FieldFactory.radio_field("status", required=True, choices=["active", "inactive"])
```

### Choice Fields

```python
# Single choice field
FieldFactory.choice_field("category", required=True, choices=["tech", "lifestyle", "news"])

# Multiple choice field
FieldFactory.multichoice_field("tags", required=True, choices=["python", "fastapi", "admin"])

# Chips field (multiple choice with chips widget)
FieldFactory.chips_field("skills", required=True, choices=["python", "javascript", "sql"])

# Listbox field (multiple choice with listbox widget)
FieldFactory.listbox_field("permissions", required=True, choices=["read", "write", "delete"])
```

### File Fields

```python
# File upload field
FieldFactory.file_field("document", required=True)

# Image field (file field with image widget)
FieldFactory.image_field("avatar", required=True)
```

### Special Fields

```python
# JSON field
FieldFactory.json_field("metadata", required=True)

# Autocomplete field
FieldFactory.autocomplete_field("search", required=True, placeholder="Start typing...")
```

## Relationship Fields

### Foreign Key Fields

```python
from .models import Category, User

# Foreign key field
FieldFactory.foreignkey_field(
    "category_id",
    model_class=Category,
    display_field="name",
    required=True
)
```

### Many-to-Many Fields

```python
# Many-to-many field
FieldFactory.many_to_many_field(
    "tags",
    model_class=Tag,
    display_field="name",
    required=False
)
```

### One-to-One Fields

```python
# One-to-one field
FieldFactory.one_to_one_field(
    "profile",
    model_class=UserProfile,
    display_field="username",
    required=False
)
```

## Field Configuration Options

All field types support these common configuration options:

```python
FieldFactory.string_field(
    "username",
    required=True,           # Field is required
    readonly=False,          # Field is read-only
    disabled=False,          # Field is disabled
    placeholder="Enter username",  # Placeholder text
    help_text="Username must be unique",  # Help text
    widget="text",           # Specific widget type
    validators=[],           # Custom validators
    custom_validator=None    # Custom validation function
)
```

### Widget Configuration

```python
# Custom widget for string field
FieldFactory.string_field(
    "phone",
    widget="phone",
    placeholder="+1 (555) 123-4567"
)

# Custom widget for choice field
FieldFactory.choice_field(
    "status",
    widget="radio",
    choices=["active", "inactive", "pending"]
)
```

## Complete Example

Here's a complete example showing all field types in use:

```python
from fp_admin.registry import ViewBuilder
from fp_admin.models.field import FieldFactory
from .models import User, Group, Permission, Department

class UserFormView(ViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        # Primary key
        FieldFactory.primary_key_field("id"),

        # Basic information
        FieldFactory.string_field("username", required=True, min_length=3, max_length=150),
        FieldFactory.string_field("first_name", required=True, max_length=100),
        FieldFactory.string_field("last_name", required=True, max_length=100),
        FieldFactory.email_field("email", required=True),

        # Security
        FieldFactory.password_field("password", required=True, min_length=8),
        FieldFactory.boolean_field("is_active", required=True),
        FieldFactory.boolean_field("is_superuser", required=True),

        # Additional information
        FieldFactory.text_field("bio", rows=4, max_length=500),

        # Relationships
        FieldFactory.foreignkey_field("department_id", model_class=Department, display_field="name"),
        FieldFactory.many_to_many_field("groups", model_class=Group, display_field="name"),
    ]

    creation_fields = ["username", "first_name", "last_name", "email", "password", "is_active", "is_superuser", "department_id"]
    allowed_update_fields = ["first_name", "last_name", "email", "is_active", "is_superuser", "bio", "department_id", "groups"]
```

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

### Validator Configuration

```python
# Field with multiple validators
FieldFactory.string_field(
    "phone",
    required=True,
    validators=[
        FpFieldValidator(
            name="format",
            condition_value=r"^\+?1?\d{9,15}$",
            error=FpFieldError(
                code="invalid_format",
                message="Phone number must be in valid format"
            )
        )
    ]
)
```

## Best Practices

### 1. Choose Appropriate Field Types

```python
# Good: Use email field for email addresses
FieldFactory.email_field("email", required=True)

# Good: Use password field for passwords
FieldFactory.password_field("password", required=True, min_length=8)

# Good: Use boolean field for true/false values
FieldFactory.boolean_field("is_active", required=True)
```

### 2. Provide Meaningful Validation

```python
# Good: Validate required fields
FieldFactory.string_field("username", required=True, min_length=3)

# Good: Validate email format
FieldFactory.email_field("email", required=True)

# Good: Validate password strength
FieldFactory.password_field("password", required=True, min_length=8)
```

### 3. Use Relationships Efficiently

```python
# Good: Use many-to-many for multiple selections
FieldFactory.many_to_many_field("groups", model_class=Group, display_field="name")

# Good: Use foreign key for single selections
FieldFactory.foreignkey_field("department_id", model_class=Department, display_field="name")
```

### 4. Organize Fields Logically

```python
fields = [
    # Primary key first
    FieldFactory.primary_key_field("id"),

    # Basic information
    FieldFactory.string_field("username", required=True),
    FieldFactory.string_field("first_name", required=True),
    FieldFactory.string_field("last_name", required=True),
    FieldFactory.email_field("email", required=True),

    # Security
    FieldFactory.password_field("password", required=True, min_length=8),
    FieldFactory.boolean_field("is_active", required=True),
    FieldFactory.boolean_field("is_superuser", required=True),

    # Relationships
    FieldFactory.many_to_many_field("groups", model_class=Group, display_field="name"),
]
```

## Performance Considerations

### 1. Field Selection

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

### 2. Relationship Loading

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

## Next Steps

- **[Widgets](../user-guide/widgets.md)** - Learn about available widgets and their configuration
- **[Admin Models](../user-guide/admin-models.md)** - Configure admin interfaces with fields
- **[Custom Fields](../advanced/custom-fields.md)** - Create custom field types and validators
- **[API Reference](../api/models.md)** - Explore the REST API endpoints
