# Welcome to fp-admin Documentation

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/status-beta-orange.svg)](https://github.com/esmairi/fp-admin)

> ⚠️ **Beta Version**: This project is currently under active development and is in beta (v0.0.6beta). APIs may change between versions. We recommend testing thoroughly in development environments before using in production.

A modern, FastAPI-based admin framework that provides automatic CRUD interfaces and admin panels for SQLModel-based applications.

## 🎨 UI Framework

The admin interface is powered by a separate React-based UI project:

- **UI Repository**: [fp-admin-ui](https://github.com/esmairi/fp-admin-ui)
- **Features**: Modern React interface with TypeScript, responsive design, and rich components
- **Integration**: Seamlessly integrates with the fp-admin backend API

## 🚀 Key Features

### 🔧 Core Architecture
- **Service-Based Architecture**: Comprehensive CRUD services with business logic separation
- **Provider System**: Flexible authentication providers (Internal, OAuth, Custom)
- **Module Loader**: Automatic discovery and loading of application components
- **Registry System**: Central management of models, views, and applications

### 📊 Admin Interface
- **Automatic Admin Interface**: Generate beautiful admin panels from SQLModel models
- **Rich Field Types**: Support for text, email, password, number, date, checkbox, textarea, file uploads, and more
- **Advanced Widgets**: Select dropdowns, radio buttons, checkbox groups, autocomplete, toggles, sliders, rich text editors
- **Relationship Support**: Handle foreign keys and many-to-many relationships

### 🔐 Authentication & Security
- **JWT Token System**: Secure access and refresh tokens with configurable expiration
- **Provider-Based Auth**: Internal authentication + extensible OAuth provider system
- **Role-Based Access Control**: Comprehensive permission and group management
- **Password Security**: Argon2-based password hashing

### 📈 API & Data
- **REST API**: Complete REST API for all models with CRUD operations
- **Form Validation**: Server-side form validation with custom error handling
- **Advanced Filtering**: Complex query building with filtering, pagination, and field selection
- **Relationship Handling**: Automatic loading and management of related data

### 🛠️ Development Tools
- **CLI Tools**: Command-line interface for project management and database operations
- **Database Migrations**: Alembic-based migration system for database schema management
- **Comprehensive Testing**: Full test suite with unit, integration, and e2e tests
- **Hot Reloading**: Development-time module reloading and debugging

## 🏗️ Architecture Overview

fp-admin is built with a modern, layered architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                        │
├─────────────────────────────────────────────────────────────┤
│                    REST API Layer                          │
├─────────────────────────────────────────────────────────────┤
│                   Services Layer                           │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐ │
│  │ CreateService│ ListService │ ReadService│UpdateService│ │
│  └─────────────┴─────────────┴─────────────┴─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                   Providers Layer                          │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐ │
│  │Internal Prov│ OAuth Prov  │Custom Prov │Auth Registry│ │
│  └─────────────┴─────────────┴─────────────┴─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                   Registry Layer                           │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐ │
│  │Model Registry│View Registry│App Registry│Module Loader│ │
│  └─────────────┴─────────────┴─────────────┴─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                   Data Layer                               │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐ │
│  │   Models    │   Views     │   Admin    │   Apps      │ │
│  └─────────────┴─────────────┴─────────────┴─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📚 Documentation Sections

### Getting Started
- **[Installation](getting-started/installation.md)** - Install fp-admin and its dependencies
- **[Quick Start](getting-started/quick-start.md)** - Create your first admin interface in minutes
- **[Core Concepts](getting-started/core-concepts.md)** - Understand the fundamental concepts

### User Guide
- **[Field Types](user-guide/field-types.md)** - Complete reference of all supported field types
- **[Widgets](user-guide/widgets.md)** - Available widgets and their configurations
- **[Admin Models](user-guide/admin-models.md)** - How to configure admin interfaces
- **[Services Layer](user-guide/services.md)** - Business logic and CRUD operations
- **[Providers](user-guide/providers.md)** - Authentication providers and OAuth integration
- **[Authentication](user-guide/authentication.md)** - User management and authentication
- **[CLI Commands](user-guide/cli-commands.md)** - Command-line interface reference

### API Reference
- **[Models API](api/models.md)** - REST API for model CRUD operations
- **[Views API](api/views.md)** - Admin view configuration API
- **[Apps API](api/apps.md)** - Application management API

### Advanced Topics
- **[Error Handling](advanced/error-handling.md)** - Custom error handling and validation
- **[Update Endpoints](advanced/update-endpoints.md)** - Advanced update operations
- **[Custom Fields](advanced/custom-fields.md)** - Creating custom field types and widgets

### Development
- **[Contributing](development/contributing.md)** - How to contribute to fp-admin
- **[Testing](development/testing.md)** - Running tests and writing new tests
- **[Building](development/building.md)** - Building and packaging fp-admin

## 🛠️ Quick Installation

```bash
# Install fp-admin
pip install fp-admin

# Or install with development dependencies
pip install fp-admin[dev]
```

## 🚀 Quick Start

```bash
# Create a new project
fp-admin startproject myapp
cd myapp

# Create an app
fp-admin startapp blog

# Set up database
fp-admin make-migrations initial
fp-admin migrate

# Create admin user
fp-admin createsuperuser

# Run the application
fp-admin run
```

Visit `http://localhost:8000/admin` to access your admin interface!

## 🔐 Authentication Setup

### Basic Authentication

```python
# main.py
from fp_admin import FastAPIAdmin
from fp_admin.apps.auth import *  # Import auth models and views

app = FastAPIAdmin()

# Authentication endpoints are automatically available at:
# POST /api/v1/auth/signup
# POST /api/v1/auth/signin
# POST /api/v1/auth/refresh
```

### Custom Authentication Provider

```python
from fp_admin.providers.internal import InternalProvider

# Configure internal provider
provider = InternalProvider(
    secret_key="your-secret-key",
    access_token_expires_minutes=30,
    refresh_token_expires_minutes=90,
    user_auth_func=your_auth_function
)
```

## 🏗️ Service Layer Usage

### Basic CRUD Operations

```python
from fp_admin.services.v1 import CreateService, ListService, ReadService, UpdateService
from fp_admin.schemas import CreateRecordParams, GetRecordsParams

# Initialize services
create_service = CreateService(User, "user")
list_service = ListService(User, "user")

# Create user
params = CreateRecordParams(data=user_data, form_id="UserForm")
user = await create_service.create_record(session, params, validate=True)

# List users with pagination
list_params = GetRecordsParams(page=1, page_size=20)
users = await list_service.list(session, list_params)
```

### Advanced Filtering

```python
# Complex filtering
filters = [
    "username__icontains=john",
    "email__endswith=@gmail.com",
    "is_active=true",
    "created_at__gte=2024-01-01"
]

params = GetRecordsParams(filters=filters)
result = await list_service.list(session, params)
```

## 📱 CLI Commands

### Project Management

```bash
# Create new project
fp-admin startproject myapp

# Create new app
fp-admin startapp blog

# Generate migrations
fp-admin make-migrations initial

# Apply migrations
fp-admin migrate

# Create superuser
fp-admin createsuperuser

# Run development server
fp-admin run
```

### Database Operations

```bash
# Check database status
fp-admin db status

# Reset database
fp-admin db reset

# Backup database
fp-admin db backup

# Restore database
fp-admin db restore
```

## 🔧 Configuration

### Environment Settings

```python
# settings.py
from fp_admin.global_settings import Settings

class MySettings(Settings):
    # Database
    DATABASE_URL = "sqlite+aiosqlite:///./app.db"

    # Security
    SECRET_KEY = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_MINUTES = 90

    # Admin
    ADMIN_PATH = "/admin"
    API_VERSION = "v1"

    # Installed apps
    INSTALLED_APPS = [
        "fp_admin.apps.auth",
        "your_app.blog",
        "your_app.users"
    ]
```

### Provider Configuration

```python
# Configure multiple authentication providers
PROVIDERS = {
    "internal": {
        "secret_key": "your-secret-key",
        "access_token_expires_minutes": 30,
        "refresh_token_expires_minutes": 90
    },
    "github": {
        "client_id": "your-github-client-id",
        "client_secret": "your-github-client-secret"
    }
}
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m unit
pytest -m integration
pytest -m e2e

# Run with coverage
pytest --cov=fp_admin

# Run specific test file
pytest tests/test_auth.py
```

### Test Configuration

```python
# tests/conftest.py
import pytest
from fp_admin import FastAPIAdmin

@pytest.fixture
def app():
    return FastAPIAdmin()

@pytest.fixture
def client(app):
    return TestClient(app)

@pytest.fixture
def session():
    # Database session for testing
    pass
```

## 📖 Examples

### Blog Application

Check out the [blog example](https://github.com/esmairi/fp-admin/tree/main/examples/blog_project) for a complete working application with:

- User authentication and authorization
- Blog posts with categories and tags
- File uploads for images
- Advanced filtering and search
- Admin interface customization

### E-commerce Application

The [e-commerce example](https://github.com/esmairi/fp-admin/tree/main/examples/ecommerce) demonstrates:

- Product catalog management
- Order processing
- User management
- Payment integration
- Inventory tracking

## 🚀 Performance Features

### Caching

```python
# Redis caching
CACHE_URL = "redis://localhost:6379"
CACHE_TTL = 3600  # 1 hour

# In-memory caching
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_user_by_id(user_id: int):
    return user_repository.get(user_id)
```

### Database Optimization

```python
# Relationship loading optimization
params = GetRecordsParams(
    fields=["id", "username", "groups"],
    include=["groups__name"]  # Only load group names
)

# Pagination
params = GetRecordsParams(page=1, page_size=50)

# Field selection
params = GetRecordsParams(fields=["id", "username", "email"])
```

## 🔒 Security Features

### Authentication Security

- **JWT Tokens**: Secure token-based authentication
- **Password Hashing**: Argon2-based password security
- **Rate Limiting**: Built-in rate limiting for API endpoints
- **CORS Protection**: Configurable CORS settings
- **Input Validation**: Comprehensive input validation and sanitization

### Authorization

- **Role-Based Access Control**: User roles and permissions
- **Field-Level Security**: Control access to specific fields
- **API Security**: Secure API endpoints with authentication
- **Audit Logging**: Track user actions and changes

## 🌟 What's New in v0.0.6beta

### Major Architecture Changes

- **Service Layer**: New comprehensive CRUD services architecture
- **Provider System**: Flexible authentication provider system
- **Enhanced Module Loading**: Improved app discovery and loading
- **Better Error Handling**: Comprehensive error handling and validation

### New Features

- **JWT Token System**: Secure access and refresh tokens
- **Advanced Filtering**: Complex query building capabilities
- **Relationship Management**: Automatic relationship field handling
- **Form Validation**: Enhanced form-based validation system

### Improvements

- **Performance**: Better database query optimization
- **Security**: Enhanced authentication and authorization
- **Developer Experience**: Improved CLI tools and debugging
- **Documentation**: Comprehensive documentation updates

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](development/contributing.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/esmairi/fp-admin.git
cd fp-admin

# Install development dependencies
uv sync --all-extras --dev

# Install git hooks
uv run pre-commit install

# Run tests
pytest

# Build documentation
mkdocs serve
```

### Contribution Areas

- **Bug Fixes**: Report and fix bugs
- **Feature Development**: Add new features
- **Documentation**: Improve documentation
- **Testing**: Add tests and improve coverage
- **Performance**: Optimize performance
- **Security**: Enhance security features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/esmairi/fp-admin/blob/main/LICENSE) file for details.

## 🔗 Links

- **GitHub**: [esmairi/fp-admin](https://github.com/esmairi/fp-admin)
- **PyPI**: [fp-admin](https://pypi.org/project/fp-admin/)
- **UI Repository**: [fp-admin-ui](https://github.com/esmairi/fp-admin-ui)
- **Documentation**: [https://esmairi.github.io/fp-admin/](https://esmairi.github.io/fp-admin/)
- **Issues**: [GitHub Issues](https://github.com/esmairi/fp-admin/issues)
- **Discussions**: [GitHub Discussions](https://github.com/esmairi/fp-admin/discussions)

## 📞 Support

### Getting Help

- **Documentation**: Start with the [Core Concepts](getting-started/core-concepts.md)
- **Examples**: Check out the [example projects](https://github.com/esmairi/fp-admin/tree/main/examples)
- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/esmairi/fp-admin/issues)
- **Discussions**: Ask questions and share ideas on [GitHub Discussions](https://github.com/esmairi/fp-admin/discussions)

### Community

- **GitHub**: Star and watch the repository
- **Discussions**: Participate in community discussions
- **Contributions**: Submit pull requests and improvements
- **Feedback**: Share your experience and suggestions

---

**Ready to get started?** Check out the [Quick Start Guide](getting-started/quick-start.md) to create your first admin interface in minutes!
