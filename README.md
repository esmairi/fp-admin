# fp-admin

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/status-beta-orange.svg)](https://github.com/esmairi/fp-admin)

> ⚠️ **Beta Version**: This project is currently under active development and is in beta (v0.0.6beta). APIs may change between versions. We recommend testing thoroughly in development environments before using in production.

A modern, FastAPI-based admin framework that provides automatic CRUD interfaces and admin panels for SQLModel-based applications.


📚 **Complete documentation is available at**: [https://esmairi.github.io/fp-admin/](https://esmairi.github.io/fp-admin/)

## 🎨 UI Framework

The admin interface is powered by a separate React-based UI project:

- **UI Repository**: [fp-admin-ui](https://github.com/esmairi/fp-admin-ui)
- **Features**: Modern React interface with TypeScript, responsive design, and rich components
- **Integration**: Seamlessly integrates with the fp-admin backend API

## 🚀 Features

- **🔧 Automatic Admin Interface**: Generate beautiful admin panels from SQLModel models
- **📊 Rich Field Types**: Support for text, email, password, number, date, checkbox, textarea, file uploads, and more
- **🎨 Advanced Widgets**: Select dropdowns, radio buttons, checkbox groups, autocomplete, toggles, sliders, rich text editors
- **🔗 Relationship Support**: Handle foreign keys and many-to-many relationships
- **✅ Validation**: Built-in field validation with custom error messages
- **🎯 Multi-Choice Fields**: Tags, chips, multi-select dropdowns with constraints
- **📝 File Uploads**: Secure file upload handling with validation and thumbnails
- **🔐 Authentication**: Built-in user management and authentication system
- **📱 CLI Tools**: Command-line interface for project management and database operations
- **⚡ FastAPI Integration**: Seamless integration with FastAPI applications
- **🧪 Comprehensive Testing**: Full test suite with unit, integration, and e2e tests
- **🎨 Modern UI**: React-based frontend with TypeScript and responsive design
- **📈 REST API**: Complete REST API for all models with CRUD operations
- **🔍 Query Builder**: Advanced query building with filtering, pagination, and field selection
- **📋 Form Validation**: Server-side form validation with custom error handling
- **🔄 Database Migrations**: Alembic-based migration system for database schema management

## 📦 Installation

### Using pip

```bash
pip install fp-admin
```


## 🔧 Dev Installation

### Using uv (Recommended)

```bash
# Install with all dependencies
uv sync --all-extras --dev

# Install git hooks
uv run pre-commit install
```

### Using pip

```bash
pip install fp-admin[dev]
```

## 🛠️ Quick Start

### 1. Create a New Project

```bash
# Create a new fp-admin project
fp-admin startproject myapp
cd myapp
```

### 2. Create an App

```bash
# Create a new app (e.g., blog)
fp-admin startapp blog
```

### 3. Set Up Database

```bash
# Create initial migration
fp-admin make-migrations initial

# Apply migrations
fp-admin migrate
```

### 4. Create Admin User

```bash
# Create a superuser account
fp-admin createsuperuser
```

### 5. Run the Application

```bash
# Start the development server
fp-admin run
```


## 📖 Documentation


📖 **GitHub Documentation**: [https://esmairi.github.io/fp-admin/](https://esmairi.github.io/fp-admin/)

The documentation includes:
- **Getting Started**: Installation, quick start, and core concepts
- **User Guide**: Field types, widgets, admin models, authentication, and CLI commands
- **API Reference**: Complete REST API documentation
- **Advanced Topics**: Error handling, custom fields, and advanced configurations
- **Development**: Contributing guidelines and testing instructions

## 📚 Core Concepts

### FieldView System

The core of fp-admin is the `FieldView` system, which provides a flexible way to define form fields:

```python
from fp_admin.admin.fields import FieldView

# Basic text field
name_field = FieldView.text_field("name", "Full Name", required=True)

# Email field with validation
email_field = FieldView.email_field("email", "Email Address")

# Multi-choice field
tags_field = MultiChoicesField.multi_choice_tags_field(
    "tags", "Tags", choices=choices, max_selections=5
)
```

### Admin Model Configuration

Define admin interfaces for your SQLModel models:

```python
from fp_admin.admin.models import AdminModel
from fp_admin.admin.fields import FieldView

class PostAdmin(AdminModel):
    model = Post
    label = "Blog Posts"
```

### Field Types and Widgets

fp-admin supports a wide variety of field types and widgets:

#### Basic Field Types
- `string`: Single-line text input (default), can be used for email, password, etc.
- `number`: Integer or numeric input
- `float`: Floating-point number input
- `boolean`: Checkbox, switch, or select for true/false values
- `date`: Date picker
- `time`: Time picker
- `datetime`: Date and time picker
- `choice`: Single-choice selection (dropdown, radio, select)
- `multichoice`: Multi-select (multiSelect, chips, listBox)
- `foreignkey`: Foreign key relationship (dropdown, autoComplete)
- `many_to_many`: Many-to-many relationship (autoComplete, dropdown)
- `OneToOneField`: One-to-one relationship (autoComplete, dropdown)
- `file`: File upload
- `image`: Image upload
- `json`: JSON editor
- `color`: Color picker
- `primarykey`: Primary key field (read-only, usually string or number)

#### Widget Types
- **Text Inputs**: `text`, `textarea`, `password`
- **Number Inputs**: `input`, `Slider`
- **Date/Time**: `calendar`
- **Boolean**: `Checkbox`, `switch`, `select`
- **Choice**: `dropdown`, `radio`, `select`
- **Multi-Choice**: `multiSelect`, `chips`, `listBox`
- **Relationship**: `dropdown`, `autoComplete`
- **File/Image**: `upload`, `image`
- **JSON**: `editor`
- **Color**: `colorPicker`

#### Advanced/Custom Widgets
- **toggle**: Boolean toggle (alias for switch)
- **richtext**: Rich text editor (uses textarea widget)
- **markdown**: Markdown editor (uses textarea widget)
- **code editor**: JSON/code editor (uses `editor` widget)
- **selectbutton**: Button-style select (uses dropdown widget)

#### Example Usage

```python
from fp_admin.admin.fields import FieldView, FieldFactory

# Basic string field
FieldView(name="title", field_type="string", widget="text")

# Email field
FieldFactory.email_field("email", "Email Address")

# Number field with slider
FieldFactory.slider_field("rating", "Rating")

# Boolean switch
FieldFactory.switch_field("is_active", "Is Active")

# Choice field (dropdown)
FieldFactory.select_field("status", "Status", options={"choices": [...]})

# Multi-choice chips
FieldFactory.chips_field("tags", "Tags")

# File upload
FieldFactory.file_field("attachment", "Attachment")

# JSON editor
FieldFactory.json_field("seo_data", "SEO Data")

# Color picker
FieldFactory.color_picker_field("color", "Color")
```

You can combine any supported field type with a compatible widget for flexible admin forms.

## 🏗️ Project Structure

```
fp-admin/
├── fp_admin/                    # Main package
│   ├── admin/                   # Admin interface
│   │   ├── fields/             # Field definitions and widgets
│   │   ├── views/              # View configurations
│   │   ├── models/             # Admin model definitions
│   │   └── apps/               # App configurations
│   ├── api/                    # REST API endpoints
│   │   └── v1/                 # API version 1
│   │       ├── models_api.py   # Model CRUD endpoints
│   │       ├── views_api.py    # View API endpoints
│   │       └── apps_api.py     # App info endpoints
│   ├── cli/                    # Command-line interface
│   ├── core/                   # Core functionality
│   ├── apps/                   # Built-in apps (auth, etc.)
│   └── services/               # Business logic services
│       ├── base.py             # Base service class
│       ├── model_service.py    # Model operations
│       ├── create_service.py   # Create operations
│       ├── read_service.py     # Read operations
│       ├── update_service.py   # Update operations
│       └── query_builder.py    # Query building
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   ├── e2e/                    # End-to-end tests
│   └── fixtures/               # Test fixtures
├── docs/                       # Documentation
├── migrations/                 # Database migrations
└── examples/                   # Example applications
```

## 📖 Examples

### Blog Application

A complete blog application demonstrating fp-admin's capabilities is included in the `examples/blog_project/` directory:

```bash
# Navigate to the blog example
cd examples/blog_project

# Install dependencies
pip install fp-admin sqlmodel fastapi uvicorn

# Set up the database
fp-admin make-migrations initial
fp-admin migrate

# Create sample data
python scripts/sample_data.py

# Run the application
python app.py
```

Features demonstrated:
- User management with authentication
- Blog post creation with rich text editor
- Category and tag management
- Comment system with moderation
- File uploads for featured images
- Admin interface customization

### Custom View Configuration

```python
from fp_admin.admin.views import BaseViewBuilder
from fp_admin.admin.fields import FieldView


# Configure admin model with custom fields
class PostFormView(BaseViewBuilder):
    model = Post
    view_type = "form"
    name = "PostForm"
    fields = [
        FieldView(name="title", label="Title", field_type="text"),
        FieldView(name="slug", label="Slug", field_type="text"),
        FieldView(
            name="content", label="Content", field_type="textarea", widget="richtext"
        ),
        FieldView(name="excerpt", label="Excerpt", field_type="textarea"),
        FieldView(name="featured_image", label="Featured Image", field_type="file"),
        FieldView(
            name="status",
            label="Status",
            field_type="select",
            widget="radio",
            options=[
                {"title": "Draft", "value": "draft"},
                {"title": "Published", "value": "published"},
                {"title": "Archived", "value": "archived"},
            ],
        ),
        FieldView(
            name="is_featured",
            label="Is Featured",
            field_type="checkbox",
            widget="toggle",
        ),
        FieldView(
            name="allow_comments",
            label="Allow Comments",
            field_type="checkbox",
            widget="switch",
        ),
    ]
```

## 🛠️ CLI Commands

### Project Management

```bash
# Create new project
fp-admin startproject myproject

# Create new app
fp-admin startapp blog

# Show project info
fp-admin info
```

### Running the Application

```bash
# Run the development server
fp-admin run

# Run with custom host and port
fp-admin run --host 0.0.0.0 --port 8080

# Run without auto-reload
fp-admin run --no-reload

# Run with different log level
fp-admin run --log-level info

# Run with custom app module
fp-admin run --app main:app
```

### Database Operations

```bash
# Create migration
fp-admin make-migrations create_tables

# Apply migrations
fp-admin migrate

# Show migration status
fp-admin database status
```

### User Management

```bash
# Create superuser
fp-admin createsuperuser

# Create regular user
fp-admin user create
```

### System Commands

```bash
# Show version
fp-admin version

# Check system status
fp-admin system status
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m unit
pytest -m integration
pytest -m e2e

# Run with coverage
pytest --cov=fp_admin
```

## 🔧 Development

### Setup Development Environment

```bash
# Install development dependencies
uv sync --all-extras --dev

# Install pre-commit hooks
uv run pre-commit install

# Run pre-commit on all files
uv run pre-commit run --all-files
```

### Code Quality

The project uses several tools for code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pre-commit**: Git hooks

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/admin/fields/test_base.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=fp_admin --cov-report=html
```

## 📄 API Reference

### FieldView Factory Methods

```python
# Basic fields
FieldView.text_field(name, title, **kwargs)
FieldView.email_field(name, title, **kwargs)
FieldView.password_field(name, title, **kwargs)
FieldView.number_field(name, title, **kwargs)
FieldView.date_field(name, title, **kwargs)
FieldView.checkbox_field(name, title, **kwargs)
FieldView.textarea_field(name, title, **kwargs)
FieldView.file_field(name, title, **kwargs)

# Widget-specific fields
FieldView.select_field(name, title, **kwargs)
FieldView.radio_field(name, title, **kwargs)
FieldView.checkbox_group_field(name, title, **kwargs)
FieldView.autocomplete_field(name, title, **kwargs)
FieldView.toggle_field(name, title, **kwargs)
FieldView.switch_field(name, title, **kwargs)
FieldView.range_field(name, title, **kwargs)
FieldView.slider_field(name, title, **kwargs)
FieldView.richtext_field(name, title, **kwargs)
FieldView.markdown_field(name, title, **kwargs)
```

### MultiChoicesField Factory Methods

```python
# Multi-choice fields
MultiChoicesField.multi_choice_select_field(name, title, choices, **kwargs)
MultiChoicesField.multi_choice_tags_field(name, title, choices, **kwargs)
MultiChoicesField.multi_choice_chips_field(name, title, choices, **kwargs)
MultiChoicesField.multi_choice_checkbox_group_field(name, title, choices, **kwargs)
```

### AdminModel Configuration

```python
class MyAdmin(AdminModel):
    model = MyModel
    label = "My Models"

    # TODO Custom actions
    actions = ["publish", "archive"]
```

## 🤝 Contributing

We welcome contributions from the community! This project is in active development and your help is greatly appreciated.

### 🚧 Development Status

- **Current Version**: Beta (0.0.3beta)
- **Development Phase**: Active development
- **API Stability**: May change between versions
- **Production Ready**: Not yet recommended for production use

### 📋 How to Contribute

#### 1. Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/your-username/fp-admin.git
cd fp-admin

# Install dependencies
uv sync --all-extras --dev

# Install pre-commit hooks
uv run pre-commit install

# Set up the database
fp-admin make-migrations initial
fp-admin migrate
```

#### 2. Choose an Area to Contribute

- **Backend Development**: Core framework, field types, validation, API endpoints
- **Frontend Development**: React UI components, TypeScript interfaces
- **Documentation**: Code docs, tutorials, examples
- **Testing**: Unit tests, integration tests, e2e tests
- **Bug Fixes**: Issue triage and resolution
- **Feature Requests**: New field types, widgets, or functionality

#### 3. Development Workflow

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Run tests
pytest

# Run linting and formatting
uv run pre-commit run --all-files

# Commit your changes
git add .
git commit -m "feat: add your feature description"

# Push to your fork
git push origin feature/your-feature-name
```

#### 4. Code Quality Standards

- **Python**: Follow PEP 8, use type hints, write docstrings
- **JavaScript/TypeScript**: Follow ESLint rules, use TypeScript
- **Tests**: Maintain >90% code coverage
- **Documentation**: Update docs for new features
- **Commits**: Use conventional commit messages

#### 5. Testing Guidelines

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m unit
pytest -m integration
pytest -m e2e

# Run with coverage
pytest --cov=fp_admin --cov-report=html

# Run linting
uv run pre-commit run --all-files
```

#### 6. Submitting Changes

1. **Create a Pull Request** from your feature branch
2. **Add a description** of your changes
3. **Link any related issues** using keywords (fixes #123, closes #456)
4. **Wait for review** from maintainers
5. **Address feedback** if requested
6. **Merge** once approved

### 🐛 Reporting Issues

When reporting issues, please include:

- **Environment**: Python version, OS, dependencies
- **Steps to reproduce**: Clear, step-by-step instructions
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Error messages**: Full error traces
- **Code examples**: Minimal code to reproduce the issue

### 💡 Feature Requests

For feature requests:

- **Describe the feature** clearly and concisely
- **Explain the use case** and why it's needed
- **Provide examples** of how it would be used
- **Consider alternatives** and discuss trade-offs

### 📚 Documentation Contributions

We welcome documentation improvements:

- **Code examples**: Clear, working examples
- **Tutorials**: Step-by-step guides
- **API documentation**: Comprehensive API reference
- **Best practices**: Development guidelines

### 🏷️ Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

### 🎯 Development Priorities

Current development priorities:

1. **API Stability**: Stabilizing the core API
2. **Field Types**: Expanding field type support
3. **UI Components**: Enhancing React components
4. **Documentation**: Comprehensive guides and examples
5. **Testing**: Improving test coverage
6. **Performance**: Optimizing for large datasets

### 📞 Getting Help

- **GitHub Issues**: [Report bugs and request features](https://github.com/esmairi/fp-admin/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/esmairi/fp-admin/discussions)
- **Code of Conduct**: [Community guidelines](CODE_OF_CONDUCT.md)

### 🙏 Acknowledgments

Thanks to all contributors who have helped shape fp-admin:

- **Core Contributors**: [List of major contributors]
- **Community Members**: Everyone who reports issues and suggests improvements
- **Open Source Projects**: FastAPI, SQLModel, Pydantic, and other dependencies

---

**Made with ❤️ by the fp-admin team**
