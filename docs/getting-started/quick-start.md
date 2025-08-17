# Quick Start

This guide will help you create your first fp-admin application in minutes.

## Prerequisites

- Python 3.12 or higher
- fp-admin installed (see [Installation](installation.md))

## Step 1: Create a New Project

```bash
# Create a new fp-admin project
fp-admin startproject myapp
cd myapp
```

This creates a new project with the following structure:

```
myapp/
├── app.py
├── settings.py
├── alembic.ini
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── apps/
```

## Step 2: Create an App

```bash
# Create a new app (e.g., blog)
fp-admin startapp blog
```

This creates a new app with models, admin registration, and view configuration.

## Step 3: Define Your Models

Edit `apps/blog/models.py` to define your models:

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Category(SQLModel, table=True):
    """Blog category model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, description="Category name")
    slug: str = Field(max_length=100, unique=True, description="URL slug")
    description: Optional[str] = Field(
        default=None, max_length=500, description="Category description"
    )
    color: Optional[str] = Field(
        default=None, max_length=7, description="Category color hex code"
    )
    is_active: bool = Field(default=True, description="Whether category is active")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )

    # Relationships
    posts: List["Post"] = Relationship(back_populates="category")

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    content: str
    published: bool = Field(default=False)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Step 4: Register Models in Admin

Edit `apps/blog/admin.py` to register your models with the admin interface:

```python
from fp_admin.registry import AdminModel
from .models import Category, Post

class CategoryAdmin(AdminModel):
    model = Category
    label = "Categories"
    display_field = "name"

class PostAdmin(AdminModel):
    model = Post
    label = "Posts"
    display_field = "title"
```

## Step 5: Create Admin Views

Edit `apps/blog/views.py` to define detailed admin views:

```python
from fp_admin.registry import ViewBuilder
from fp_admin.models.field import FieldFactory
from .models import Category, Post

class CategoryFormView(ViewBuilder):
    model = Category
    view_type = "form"
    name = "CategoryForm"
    fields = [
        FieldFactory.primary_key_field("id"),
        FieldFactory.string_field("name", required=True, max_length=100),
        FieldFactory.string_field("slug", required=True, max_length=100),
        FieldFactory.text_field("description", max_length=500),
        FieldFactory.string_field("color", max_length=7),
        FieldFactory.boolean_field("is_active"),
        FieldFactory.datetime_field("created_at"),
        FieldFactory.datetime_field("updated_at"),
    ]

    creation_fields = ["name", "slug", "description", "color", "is_active"]
    allowed_update_fields = ["name", "slug", "description", "color", "is_active"]
```

## Step 6: Register Your App

Edit `apps/blog/apps.py` to register your app:

```python
from fp_admin.registry import AppConfig

class BlogConfig(AppConfig):
    name = "blog"
    verbose_name = "my blog"
```

## Step 7: Set Up Database

```bash
# Create initial migration
fp-admin make-migrations initial

# Apply migrations
fp-admin migrate
```

## Step 8: Create Admin User

```bash
# Create a superuser account
fp-admin createsuperuser
```

Follow the prompts to create your admin user.

## Step 9: Run the Application

```bash
# Start the development server
fp-admin run
```

Visit `http://localhost:8000/admin` to access your admin interface!

## Step 10: Add Sample Data

You can add sample data programmatically:

```python
# In a Python shell or script
from apps.blog.models import Category, Post
from fp_admin.core.db import db_manager

async with db_manager.get_session() as session:
    # Create categories
    tech = Category(name="Technology", description="Tech-related posts")
    lifestyle = Category(name="Lifestyle", description="Lifestyle posts")
    session.add(tech)
    session.add(lifestyle)
    session.commit()

    # Create posts
    post1 = Post(
        title="Getting Started with fp-admin",
        content="fp-admin is a modern admin framework...",
        published=True,
        category_id=tech.id
    )
    session.add(post1)
    session.commit()
```

## Understanding the Two-Step Approach

fp-admin uses a two-step approach for admin configuration:

### 1. Admin Registration (admin.py)
Simple model registration that tells fp-admin which models to include in the admin interface:

```python
class PostAdmin(AdminModel):
    model = Post
    label = "Posts"
    display_field = "title"
```

### 2. View Configuration (views.py)
Detailed configuration that defines how forms and lists appear:

```python
class PostFormView(ViewBuilder):
    model = Post
    view_type = "form"
    name = "PostForm"
    fields = [
        FieldFactory.primary_key_field("id"),
        FieldFactory.string_field("title", required=True),
        FieldFactory.text_field("content", required=True),
        FieldFactory.boolean_field("published"),
        FieldFactory.foreignkey_field("category_id", model_class=Category, display_field="name"),
    ]
```

## Advanced Configuration

### Custom Settings

Edit `settings.py` to customize your application:

```python
from fp_admin.global_settings import *

# Database
DATABASE_URL = "sqlite:///./app.db"

# Admin Settings
ADMIN_TITLE = "My Blog Admin"
ADMIN_DESCRIPTION = "Admin interface for my blog"

# Security
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# File Upload
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

### Custom Field Types

You can create custom field types:

```python
from fp_admin.models.field import FieldFactory

# Custom rich text field
class RichTextField(FieldFactory):
    def __init__(self, name: str, **kwargs):
        super().__init__(
            name=name,
            field_type="string",
            widget="richtext",
            **kwargs
        )
```

### API Endpoints

Your models automatically get REST API endpoints:

- `GET /api/v1/models/category/` - List categories
- `POST /api/v1/models/category/` - Create category
- `GET /api/v1/models/category/{id}` - Get category
- `PUT /api/v1/models/category/{id}` - Update category
- `DELETE /api/v1/models/category/{id}` - Delete category

## Next Steps

Now that you have a basic application running, explore:

- **[Field Types](../user-guide/field-types.md)** - Learn about all available field types
- **[Widgets](../user-guide/widgets.md)** - Discover advanced widgets and configurations
- **[Admin Models](../user-guide/admin-models.md)** - Configure advanced admin features
- **[Authentication](../user-guide/authentication.md)** - Set up user management
- **[CLI Commands](../user-guide/cli-commands.md)** - Learn about command-line tools

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check your `DATABASE_URL` in `settings.py`
   - Ensure the database file is writable

2. **Import Errors**
   - Make sure all apps are properly registered
   - Check that models are imported correctly

3. **Migration Issues**
   - Delete the `migrations/versions/` directory and recreate migrations
   - Check for model import issues

4. **Admin Interface Not Loading**
   - Check that views are properly registered
   - Verify field configurations

For more help, check the [Advanced Topics](../advanced/error-handling.md) section or [open an issue](https://github.com/esmairi/fp-admin/issues).
