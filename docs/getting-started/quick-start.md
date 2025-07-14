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

This creates a new app with models, views, and admin configuration.

## Step 3: Define Your Models

Edit `apps/blog/models.py` to define your models:

```python
from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    content: str
    published: bool = Field(default=False)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Step 4: Create Admin Views

Edit `apps/blog/views.py` to define admin views:

```python
from fp_admin.admin.views import AdminView
from fp_admin.admin.fields import FieldView
from .models import Category, Post

class CategoryView(AdminView):
    model = Category
    label = "Categories"
    list_fields = ["id", "name", "description", "created_at"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]

    def get_form_fields(self):
        return [
            FieldView.text_field("name", "Name", required=True),
            FieldView.textarea_field("description", "Description"),
        ]

class PostView(AdminView):
    model = Post
    label = "Blog Posts"

    def get_form_fields(self):
        return [
            FieldView.text_field("title", "Title", required=True),
            FieldView.textarea_field("content", "Content", required=True),
            FieldView.switch_field("published", "Published"),
            FieldView.foreign_key_field("category_id", "Category", model=Category),
        ]
```

## Step 5: Register Your App

Edit `apps/blog/apps.py` to register your app:

```python
from fp_admin.apps import AppConfig

class BlogConfig(AppConfig):
    name = "blog"
    label = "blog"
    views = [
        "apps.blog.views.CategoryView",
        "apps.blog.views.PostView",
    ]
```

## Step 6: Set Up Database

```bash
# Create initial migration
fp-admin make-migrations initial

# Apply migrations
fp-admin migrate
```

## Step 7: Create Admin User

```bash
# Create a superuser account
fp-admin createsuperuser
```

Follow the prompts to create your admin user.

## Step 8: Run the Application

```bash
# Start the development server
fp-admin run
```

Visit `http://localhost:8000/admin` to access your admin interface!

## Step 9: Add Sample Data

You can add sample data programmatically:

```python
# In a Python shell or script
from app import engine
from apps.blog.models import Category, Post
from sqlmodel import Session

with Session(engine) as session:
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
from fp_admin.admin.fields import FieldView

# Custom rich text field
class RichTextField(FieldView):
    def __init__(self, name: str, label: str, **kwargs):
        super().__init__(
            name=name,
            label=label,
            field_type="string",
            widget="richtext",
            **kwargs
        )

# Usage in views
def get_form_fields(self):
    return [
        FieldView.text_field("title", "Title"),
        RichTextField("content", "Content"),
    ]
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
