# Widgets

This guide covers all available widgets in fp-admin and how to configure them.

## Overview

Widgets are the UI components that render form fields in the admin interface. Each field type supports specific widgets that determine how the field appears and behaves. In fp-admin, widgets are automatically selected based on the field type when using `FieldFactory`.

## Field Factory Widgets

### Text Widget

Single-line text input for short text.

```python
from fp_admin.admin.fields import FieldFactory

# Basic text field
FieldFactory.string_field("name", "Name", required=True)

# With max length
FieldFactory.string_field("title", "Title", max_length=100)

# With pattern validation
FieldFactory.string_field("phone", "Phone", pattern=r"^\+?1?\d{9,15}$")
```

**Configuration Options:**
- `required`: Whether the field is required
- `max_length`: Maximum character length
- `min_length`: Minimum character length
- `pattern`: Regex pattern for validation

### Email Widget

Email input with built-in validation.

```python
# Basic email field
FieldFactory.email_field("email", "Email", required=True)

# With custom validation
FieldFactory.email_field("contact_email", "Contact Email", required=True)
```

**Configuration Options:**
- `required`: Whether the field is required

### Password Widget

Password input with hidden characters.

```python
# Basic password field
FieldFactory.password_field("password", "Password", required=True, min_length=8)

# With strength requirements
FieldFactory.password_field("new_password", "New Password", required=True, min_length=8)
```

**Configuration Options:**
- `required`: Whether the field is required
- `min_length`: Minimum password length

### Textarea Widget

Multi-line text input for longer content.

```python
# Basic textarea
FieldFactory.textarea_field("description", "Description")

# With rows
FieldFactory.textarea_field("content", "Content", rows=10)

# With max length
FieldFactory.textarea_field("notes", "Notes", rows=5, max_length=500)
```

**Configuration Options:**
- `rows`: Number of visible rows
- `max_length`: Maximum character length

### Boolean Widget

Toggle switch for true/false values.

```python
# Basic boolean field
FieldFactory.boolean_field("is_active", "Active")

# With default value
FieldFactory.boolean_field("newsletter", "Newsletter", default=True)
```

**Configuration Options:**
- `default`: Default checked state

### Primary Key Widget

Readonly field for primary keys.

```python
# Primary key field (always readonly)
FieldFactory.primarykey_field("id", "ID")
```

**Configuration Options:**
- Always readonly and disabled
- No additional configuration needed

## Relationship Widgets

### Many-to-Many Widget

Multi-select for many-to-many relationships.

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
```

**Configuration Options:**
- `model_class`: The related model class
- `field_title`: The field to display from the related model

### Foreign Key Widget

Single-select dropdown for foreign key relationships.

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

**Configuration Options:**
- `model_class`: The related model class
- `field_title`: The field to display from the related model

## Widget Configuration Examples

### User Form Widgets

```python
from fp_admin.admin.fields import FieldFactory
from .models import User, Group

class UserFormView(BaseViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        # Readonly primary key
        FieldFactory.primarykey_field("id", "ID"),

        # Text inputs
        FieldFactory.string_field("username", "Username", required=True, min_length=3),
        FieldFactory.string_field("first_name", "First Name", required=True),
        FieldFactory.string_field("last_name", "Last Name", required=True),

        # Email input
        FieldFactory.email_field("email", "Email", required=True),

        # Password input
        FieldFactory.password_field("password", "Password", required=True, min_length=8),

        # Boolean toggles
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),

        # Textarea for longer content
        FieldFactory.textarea_field("bio", "Biography", rows=4, max_length=500),

        # Many-to-many selection
        FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name"),
    ]
```

### Group Form Widgets

```python
class GroupFormView(BaseViewBuilder):
    model = Group
    view_type = "form"
    name = "GroupForm"

    fields = [
        # Readonly primary key
        FieldFactory.primarykey_field("id", "ID"),

        # Text inputs
        FieldFactory.string_field("name", "Name", required=True, min_length=1),
        FieldFactory.string_field("description", "Description", required=True, min_length=1, max_length=200),

        # Many-to-many selections
        FieldFactory.many_to_many_field("permissions", "Permissions", model_class=Permission, field_title="name"),
        FieldFactory.many_to_many_field("users", "Users", model_class=User, field_title="username"),
    ]
```

### Permission Form Widgets

```python
class PermissionFormView(BaseViewBuilder):
    model = Permission
    view_type = "form"
    name = "PermissionForm"

    fields = [
        # Readonly primary key
        FieldFactory.primarykey_field("id", "ID"),

        # Text inputs
        FieldFactory.string_field("codename", "Code Name", required=True, min_length=1, max_length=150),
        FieldFactory.string_field("name", "Name", required=True, min_length=1, max_length=150),
        FieldFactory.string_field("description", "Description", required=True, min_length=1, max_length=200),

        # Many-to-many selection
        FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name"),
    ]
```

## Widget Behavior

### Form Widgets

Form widgets are used in create and edit forms:

- **Text inputs**: Single-line text entry
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
- **Primary key**: Plain number display
- **Relationships**: Display related object names

## Widget Validation

### Client-Side Validation

```python
# Required field validation
FieldFactory.string_field("username", "Username", required=True)

# Length validation
FieldFactory.string_field("title", "Title", min_length=1, max_length=200)

# Pattern validation
FieldFactory.string_field("phone", "Phone", pattern=r"^\+?1?\d{9,15}$")

# Email validation
FieldFactory.email_field("email", "Email", required=True)

# Password strength
FieldFactory.password_field("password", "Password", required=True, min_length=8)
```

### Server-Side Validation

All field validations are also enforced on the server side:

- Required field checking
- Length constraints
- Pattern matching
- Email format validation
- Password strength requirements
- Relationship integrity

## Widget Styling

### Default Styling

All widgets come with consistent styling:

- **Text inputs**: Clean, modern appearance
- **Email inputs**: Email-specific styling
- **Password inputs**: Secure appearance with strength indicators
- **Textarea**: Resizable with proper padding
- **Boolean toggles**: Modern switch appearance
- **Dropdowns**: Searchable with clear options
- **Multi-select**: Tag-like appearance for selected items

### Responsive Design

All widgets are responsive:

- **Mobile**: Touch-friendly controls
- **Tablet**: Optimized for touch and mouse
- **Desktop**: Full keyboard and mouse support

## Widget Accessibility

### Accessibility Features

All widgets include accessibility features:

- **Screen readers**: Proper ARIA labels
- **Keyboard navigation**: Full keyboard support
- **Focus management**: Clear focus indicators
- **Color contrast**: WCAG compliant colors
- **Error messages**: Clear, descriptive errors

### Keyboard Shortcuts

- **Tab**: Navigate between fields
- **Enter**: Submit forms
- **Escape**: Cancel or close dialogs
- **Arrow keys**: Navigate dropdowns and lists

## Widget Performance

### Optimization Features

Widgets are optimized for performance:

- **Lazy loading**: Load data as needed
- **Debounced search**: Efficient search in dropdowns
- **Virtual scrolling**: Handle large lists efficiently
- **Caching**: Cache frequently used data

### Best Practices

```python
# Use appropriate field types
FieldFactory.email_field("email", "Email")  # Better than string_field for emails
FieldFactory.boolean_field("is_active", "Active")  # Better than choice_field for booleans

# Provide meaningful validation
FieldFactory.string_field("username", "Username", required=True, min_length=3)

# Use relationships efficiently
FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name")
```

## Widget Customization

### Field-Level Customization

```python
# Custom validation messages
FieldFactory.string_field(
    "username",
    "Username",
    required=True,
    min_length=3,
    max_length=50
)

# Custom field behavior
FieldFactory.textarea_field(
    "description",
    "Description",
    rows=5,
    max_length=1000
)
```

### View-Level Customization

```python
class CustomUserFormView(BaseViewBuilder):
    model = User
    view_type = "form"
    name = "CustomUserForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("username", "Username", required=True),
        FieldFactory.email_field("email", "Email", required=True),
        FieldFactory.password_field("password", "Password", required=True, min_length=8),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name"),
    ]

    creation_fields = ["username", "email", "password", "is_active"]
    allowed_update_fields = ["email", "is_active", "groups"]
```

## Widget Testing

### Testing Widget Behavior

```python
import pytest
from fp_admin.admin.fields import FieldFactory

def test_string_field_validation():
    """Test string field validation"""
    field = FieldFactory.string_field("username", "Username", required=True, min_length=3)

    # Test validation
    assert field.required is True
    assert field.min_length == 3

def test_email_field_validation():
    """Test email field validation"""
    field = FieldFactory.email_field("email", "Email", required=True)

    # Test validation
    assert field.required is True
    assert field.field_type == "email"

def test_boolean_field_behavior():
    """Test boolean field behavior"""
    field = FieldFactory.boolean_field("is_active", "Active")

    # Test behavior
    assert field.field_type == "boolean"
```

## Widget Best Practices

### 1. Choose Appropriate Widgets

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
# Good: Validate required fields
FieldFactory.string_field("username", "Username", required=True, min_length=3)

# Good: Validate email format
FieldFactory.email_field("email", "Email", required=True)

# Good: Validate password strength
FieldFactory.password_field("password", "Password", required=True, min_length=8)
```

### 3. Use Relationships Efficiently

```python
# Good: Use many-to-many for multiple selections
FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name")

# Good: Use foreign key for single selections
FieldFactory.foreign_key_field("department_id", "Department", model_class=Department, field_title="name")
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

    # Relationships
    FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name"),
]
```

## Next Steps

- **[Field Types](field-types.md)** - Learn about all available field types
- **[Admin Models](admin-models.md)** - Configure admin interfaces
- **[Authentication](authentication.md)** - Set up user management
- **[CLI Commands](cli-commands.md)** - Learn about development tools
