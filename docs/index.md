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

## 📚 Documentation Sections

### Getting Started
- **[Installation](getting-started/installation.md)** - Install fp-admin and its dependencies
- **[Quick Start](getting-started/quick-start.md)** - Create your first admin interface in minutes
- **[Core Concepts](getting-started/core-concepts.md)** - Understand the fundamental concepts

### User Guide
- **[Field Types](user-guide/field-types.md)** - Complete reference of all supported field types
- **[Widgets](user-guide/widgets.md)** - Available widgets and their configurations
- **[Admin Models](user-guide/admin-models.md)** - How to configure admin interfaces
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

## 📖 Examples

Check out the [blog example](https://github.com/esmairi/fp-admin/tree/main/examples/blog_project) for a complete working application.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](development/contributing.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/esmairi/fp-admin/blob/main/LICENSE) file for details.

## 🔗 Links

- **GitHub**: [esmairi/fp-admin](https://github.com/esmairi/fp-admin)
- **PyPI**: [fp-admin](https://pypi.org/project/fp-admin/)
- **UI Repository**: [fp-admin-ui](https://github.com/esmairi/fp-admin-ui)
- **Issues**: [GitHub Issues](https://github.com/esmairi/fp-admin/issues)
- **Discussions**: [GitHub Discussions](https://github.com/esmairi/fp-admin/discussions)
