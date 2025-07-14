# Admin Models

This guide explains how to configure admin models in fp-admin to create powerful admin interfaces.

## Overview

fp-admin uses a two-step approach for admin configuration:

1. **Admin Registration** (`admin.py`) - Simple model registration
2. **View Configuration** (`views.py`) - Detailed interface configuration

This separation keeps model registration simple while allowing detailed customization in views.

## Admin Registration (admin.py)

Admin registration is the simple process of registering your models with the admin interface:

```python
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

### Admin Registration Features

- **Simple Setup**: Just specify the model and label
- **Automatic Discovery**: Models are automatically discovered by the admin interface
- **Clean Separation**: Keeps model registration separate from view configuration
- **Minimal Code**: Requires only the essential information

### Required Attributes

- **model**: The SQLModel class to register
- **label**: Display name in the admin interface

## View Configuration (views.py)

Views define the detailed configuration of how your models appear in the admin interface using `BaseViewBuilder`:

```python
from fp_admin.admin.views import BaseViewBuilder
from fp_admin.admin.fields import FieldFactory
from .models import User, Group, Permission

class UserFormView(BaseViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("username", "Username", required=True),
        FieldFactory.email_field("email", "Email", required=True),
        FieldFactory.password_field("password", "Password", required=True, min_length=8),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),
        FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name"),
    ]

    creation_fields = ["username", "email", "password", "is_active", "is_superuser"]
    allowed_update_fields = ["email", "is_active", "is_superuser"]
```

## View Types

fp-admin supports different view types for different purposes:

### Form Views

For creating and editing records:

```python
class UserFormView(BaseViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("username", "Username", required=True),
        FieldFactory.email_field("email", "Email", required=True),
        FieldFactory.password_field("password", "Password", required=True),
        FieldFactory.boolean_field("is_active", "Active"),
    ]

    creation_fields = ["username", "email", "password", "is_active"]
    allowed_update_fields = ["email", "is_active"]
```

### List Views

For displaying records in a table format:

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

## Model Configuration

### Required Attributes

- **model**: The SQLModel class to administer
- **view_type**: Type of view ("form" or "list")
- **name**: Unique name for the view

### Optional Attributes

- **fields**: List of field configurations
- **creation_fields**: Fields allowed during creation
- **allowed_update_fields**: Fields allowed during updates

## Field Configuration

### Basic Field Types

```python
# Primary key field (readonly)
FieldFactory.primarykey_field("id", "ID")

# String field
FieldFactory.string_field("username", "Username", required=True, min_length=3)

# Email field
FieldFactory.email_field("email", "Email", required=True)

# Password field
FieldFactory.password_field("password", "Password", required=True, min_length=8)

# Boolean field
FieldFactory.boolean_field("is_active", "Active")

# Text area field
FieldFactory.textarea_field("description", "Description", rows=5)
```

### Relationship Fields

```python
# Many-to-many relationship
FieldFactory.many_to_many_field(
    "groups",
    "Groups",
    model_class=Group,
    field_title="name"
)

# Foreign key relationship
FieldFactory.foreign_key_field(
    "category_id",
    "Category",
    model_class=Category,
    field_title="name"
)
```

### Field Configuration Options

```python
# String field with validation
FieldFactory.string_field(
    "title",
    "Title",
    required=True,
    min_length=1,
    max_length=200
)

# Email field with pattern validation
FieldFactory.email_field(
    "email",
    "Email",
    required=True
)

# Password field with strength requirements
FieldFactory.password_field(
    "password",
    "Password",
    required=True,
    min_length=8
)
```

## Complete Example

Here's a complete example based on the auth app:

```python
from fp_admin.admin.views import BaseViewBuilder
from fp_admin.admin.fields import FieldFactory
from .models import User, Group, Permission

# User Form View
class UserFormView(BaseViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("username", "Username", required=True),
        FieldFactory.email_field("email", "Email", required=True),
        FieldFactory.password_field("password", "Password", required=True, min_length=8),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),
        FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name"),
    ]

    creation_fields = ["username", "email", "password", "is_active", "is_superuser"]
    allowed_update_fields = ["email", "is_active", "is_superuser"]

# User List View
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

# Group Form View
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

    creation_fields = ["name", "description"]
    allowed_update_fields = ["name", "description", "permissions"]
```

## Best Practices

1. **Use descriptive names**: Choose clear, descriptive names for your views
2. **Separate concerns**: Use different views for different operations (form vs list)
3. **Validate fields**: Always specify required fields and validation rules
4. **Control updates**: Use `allowed_update_fields` to restrict what can be changed
5. **Use relationships**: Leverage `many_to_many_field` and `foreign_key_field` for relationships
6. **Follow naming conventions**: Use consistent naming patterns across your views
