# Widgets

Widgets are the UI components that render form fields in the admin interface. fp-admin provides a variety of widgets that automatically map to different field types, and you can customize widget behavior for specific use cases.

## Overview

Widgets are automatically selected based on the field type, but you can override them to provide custom UI components. Each widget type offers specific configuration options to enhance the user experience.

## Widget Types

### Text Widgets

#### String Input Widget

```python
from fp_admin.models.field import FieldFactory

# Basic string input
FieldFactory.string_field("username", required=True, placeholder="Enter username")

# With custom widget
FieldFactory.string_field("phone", widget="phone", placeholder="+1 (555) 123-4567")
```

#### Text Area Widget

```python
# Multi-line text input
FieldFactory.text_field("description", placeholder="Enter description", rows=5)

# With custom configuration
FieldFactory.text_field("bio", rows=4, max_length=500, placeholder="Tell us about yourself")
```

#### Email Widget

```python
# Email input with validation
FieldFactory.email_field("email", required=True, placeholder="Enter email address")
```

#### Password Widget

```python
# Password input with hidden characters
FieldFactory.password_field("password", required=True, min_length=8, placeholder="Enter password")
```

### Numeric Widgets

#### Number Input Widget

```python
# Integer input
FieldFactory.number_field("age", required=True, placeholder="Enter age")

# With range constraints
FieldFactory.number_field("rating", min_value=1, max_value=5, step=1)
```

#### Float Input Widget

```python
# Decimal number input
FieldFactory.float_field("price", required=True, placeholder="Enter price")

# With precision
FieldFactory.float_field("score", min_value=0.0, max_value=10.0, step=0.1)
```

#### Slider Widget

```python
# Slider for number selection
FieldFactory.slider_field("rating", min_value=1, max_value=5, step=1)
```

### Date and Time Widgets

#### Date Widget

```python
# Date picker
FieldFactory.date_field("birth_date", required=True)
```

#### Time Widget

```python
# Time picker
FieldFactory.time_field("appointment_time", required=True)
```

#### DateTime Widget

```python
# Date and time picker
FieldFactory.datetime_field("created_at", required=True)
```

### Boolean Widgets

#### Checkbox Widget

```python
# Standard checkbox
FieldFactory.boolean_field("is_active", required=True)
```

#### Toggle Widget

```python
# Switch/toggle widget
FieldFactory.toggle_field("is_verified", required=True)
```

#### Radio Widget

```python
# Radio button group
FieldFactory.radio_field("status", required=True, choices=["active", "inactive", "pending"])
```

### Choice Widgets

#### Select Widget

```python
# Dropdown selection
FieldFactory.choice_field("category", required=True, choices=["tech", "lifestyle", "news"])
```

#### Multi-Select Widget

```python
# Multiple choice selection
FieldFactory.multichoice_field("tags", required=True, choices=["python", "fastapi", "admin"])
```

#### Chips Widget

```python
# Multiple choice with chips display
FieldFactory.chips_field("skills", required=True, choices=["python", "javascript", "sql"])
```

#### Listbox Widget

```python
# Multiple choice with listbox display
FieldFactory.listbox_field("permissions", required=True, choices=["read", "write", "delete"])
```

### File Widgets

#### File Upload Widget

```python
# File upload
FieldFactory.file_field("document", required=True)
```

#### Image Widget

```python
# Image upload with preview
FieldFactory.image_field("avatar", required=True)
```

### Special Widgets

#### JSON Widget

```python
# JSON editor
FieldFactory.json_field("metadata", required=True)
```

#### Autocomplete Widget

```python
# Autocomplete input
FieldFactory.autocomplete_field("search", required=True, placeholder="Start typing...")
```

## Relationship Widgets

### Foreign Key Widget

```python
from .models import Category, Department

# Single selection from related model
FieldFactory.foreignkey_field(
    "category_id",
    model_class=Category,
    display_field="name",
    required=True
)

# With custom configuration
FieldFactory.foreignkey_field(
    "department_id",
    model_class=Department,
    display_field="name",
    required=True,
    placeholder="Select department"
)
```

### Many-to-Many Widget

```python
# Multiple selection from related model
FieldFactory.many_to_many_field(
    "tags",
    model_class=Tag,
    display_field="name",
    required=False
)

# With custom widget
FieldFactory.many_to_many_field(
    "groups",
    model_class=Group,
    display_field="name",
    required=False,
    widget="chips"
)
```

### One-to-One Widget

```python
# Single selection for one-to-one relationship
FieldFactory.one_to_one_field(
    "profile",
    model_class=UserProfile,
    display_field="username",
    required=False
)
```

## Widget Configuration

### Common Widget Options

All widgets support these common configuration options:

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

### Widget-Specific Options

#### Text Widgets

```python
# String field with custom widget
FieldFactory.string_field(
    "phone",
    widget="phone",
    placeholder="+1 (555) 123-4567",
    pattern=r"^\+?1?\d{9,15}$"
)

# Text area with custom configuration
FieldFactory.text_field(
    "description",
    rows=5,
    max_length=1000,
    placeholder="Enter detailed description"
)
```

#### Numeric Widgets

```python
# Number field with constraints
FieldFactory.number_field(
    "rating",
    min_value=1,
    max_value=5,
    step=1,
    placeholder="Select rating"
)

# Slider with custom range
FieldFactory.slider_field(
    "progress",
    min_value=0,
    max_value=100,
    step=5,
    placeholder="Set progress"
)
```

#### Choice Widgets

```python
# Choice field with custom widget
FieldFactory.choice_field(
    "status",
    widget="radio",
    choices=["active", "inactive", "pending"],
    required=True
)

# Multi-choice with custom widget
FieldFactory.multichoice_field(
    "skills",
    widget="chips",
    choices=["python", "javascript", "sql", "html", "css"],
    required=False
)
```

## Complete Example

Here's a complete example showing various widgets in use:

```python
from fp_admin.registry import ViewBuilder
from fp_admin.models.field import FieldFactory
from .models import User, Group, Department

class UserFormView(ViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        # Primary key (readonly)
        FieldFactory.primary_key_field("id"),

        # Basic information with custom widgets
        FieldFactory.string_field("username", required=True, placeholder="Enter username"),
        FieldFactory.string_field("first_name", required=True, placeholder="Enter first name"),
        FieldFactory.string_field("last_name", required=True, placeholder="Enter last name"),
        FieldFactory.email_field("email", required=True, placeholder="Enter email address"),

        # Security fields
        FieldFactory.password_field("password", required=True, min_length=8, placeholder="Enter password"),
        FieldFactory.toggle_field("is_active", required=True),  # Switch widget
        FieldFactory.radio_field("role", required=True, choices=["user", "admin", "moderator"]),

        # Additional information
        FieldFactory.text_field("bio", rows=4, max_length=500, placeholder="Tell us about yourself"),
        FieldFactory.number_field("age", min_value=13, max_value=120, placeholder="Enter age"),

        # Relationships
        FieldFactory.foreignkey_field(
            "department_id",
            model_class=Department,
            display_field="name",
            required=True,
            placeholder="Select department"
        ),
        FieldFactory.many_to_many_field(
            "groups",
            model_class=Group,
            display_field="name",
            required=False,
            widget="chips"  # Use chips widget
        ),
    ]

    creation_fields = ["username", "first_name", "last_name", "email", "password", "is_active", "role", "age", "department_id"]
    allowed_update_fields = ["first_name", "last_name", "email", "is_active", "role", "bio", "age", "department_id", "groups"]
```

## Widget Behavior

### Form Widgets

Form widgets are used in create and edit forms:

- **Text inputs**: Single-line text entry with validation
- **Email inputs**: Email validation with proper keyboard on mobile
- **Password inputs**: Hidden characters with strength indicators
- **Textarea**: Multi-line text entry with resizable area
- **Boolean toggles**: Switch-style true/false controls
- **Many-to-many**: Multi-select dropdown with search
- **Foreign key**: Single-select dropdown with search

### List Widgets

List widgets are used in table displays:

- **Text fields**: Plain text display
- **Email fields**: Clickable email links
- **Boolean fields**: Checkmark or toggle display
- **Date fields**: Formatted date display
- **Relationship fields**: Related object display

## Custom Widget Configuration

### Overriding Default Widgets

You can override the default widget for any field type:

```python
# Use radio buttons instead of dropdown for choice field
FieldFactory.choice_field(
    "status",
    widget="radio",  # Override default "select" widget
    choices=["active", "inactive", "pending"],
    required=True
)

# Use chips instead of listbox for multi-choice
FieldFactory.multichoice_field(
    "tags",
    widget="chips",  # Override default widget
    choices=["python", "fastapi", "admin"],
    required=False
)
```

### Widget-Specific Configuration

```python
# Custom placeholder for specific widget
FieldFactory.string_field(
    "phone",
    widget="phone",
    placeholder="+1 (555) 123-4567"
)

# Custom configuration for number field
FieldFactory.number_field(
    "rating",
    min_value=1,
    max_value=5,
    step=1,
    placeholder="Select rating from 1 to 5"
)
```

## Widget Testing

### Testing Widget Behavior

```python
import pytest
from fp_admin.models.field import FieldFactory

def test_string_field_widget():
    """Test string field widget configuration"""
    field = FieldFactory.string_field("username", required=True, placeholder="Enter username")

    # Test widget configuration
    assert field.widget is None  # Default widget
    assert field.placeholder == "Enter username"
    assert field.required is True

def test_choice_field_widget():
    """Test choice field widget configuration"""
    field = FieldFactory.choice_field("status", widget="radio", choices=["active", "inactive"])

    # Test widget configuration
    assert field.widget == "radio"
    assert field.field_type == "choice"

def test_boolean_field_widget():
    """Test boolean field widget behavior"""
    field = FieldFactory.boolean_field("is_active", required=True)

    # Test widget configuration
    assert field.field_type == "boolean"
    assert field.required is True
```

## Widget Best Practices

### 1. Choose Appropriate Widgets

```python
# Good: Use toggle for boolean fields
FieldFactory.toggle_field("is_active", required=True)

# Good: Use radio for small choice sets
FieldFactory.radio_field("status", choices=["active", "inactive"], required=True)

# Good: Use chips for multiple selections
FieldFactory.chips_field("tags", choices=["python", "fastapi"], required=False)
```

### 2. Provide Meaningful Placeholders

```python
# Good: Clear, descriptive placeholders
FieldFactory.string_field("username", placeholder="Enter unique username")
FieldFactory.email_field("email", placeholder="Enter valid email address")
FieldFactory.number_field("age", placeholder="Enter age (13-120)")
```

### 3. Use Widgets Efficiently

```python
# Good: Use appropriate widgets for data types
FieldFactory.toggle_field("is_verified", required=True)  # Boolean
FieldFactory.choice_field("category", choices=["tech", "lifestyle"], required=True)  # Single choice
FieldFactory.chips_field("skills", choices=["python", "javascript"], required=False)  # Multiple choice
```

### 4. Organize Fields Logically

```python
fields = [
    # Primary key first
    FieldFactory.primary_key_field("id"),

    # Basic information
    FieldFactory.string_field("username", required=True, placeholder="Enter username"),
    FieldFactory.email_field("email", required=True, placeholder="Enter email"),

    # Security
    FieldFactory.password_field("password", required=True, placeholder="Enter password"),
    FieldFactory.toggle_field("is_active", required=True),

    # Relationships
    FieldFactory.many_to_many_field("groups", model_class=Group, display_field="name"),
]
```

## Performance Considerations

### 1. Widget Selection

Choose widgets that provide the best user experience without compromising performance:

```python
# Good: Use chips for small choice sets
FieldFactory.chips_field("status", choices=["active", "inactive", "pending"])

# Good: Use listbox for large choice sets
FieldFactory.listbox_field("permissions", choices=large_permission_list)
```

### 2. Relationship Loading

Configure relationship widgets efficiently:

```python
# Good: Specify display fields for performance
FieldFactory.foreignkey_field(
    "category_id",
    model_class=Category,
    display_field="name",  # Only load the name field
    required=True
)
```

## Next Steps

- **[Field Types](../user-guide/field-types.md)** - Learn about all available field types
- **[Admin Models](../user-guide/admin-models.md)** - Configure admin interfaces with widgets
- **[Custom Fields](../advanced/custom-fields.md)** - Create custom widgets and field types
- **[API Reference](../api/models.md)** - Explore the REST API endpoints
