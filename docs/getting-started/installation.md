# Installation

This guide will help you install fp-admin and its dependencies.

## Prerequisites

- Python 3.12 or higher
- pip or uv package manager
- Git (for development)

## Installation Methods

### Using pip (Recommended for Production)

```bash
# Install fp-admin
pip install fp-admin

# Install with development dependencies
pip install fp-admin[dev]
```

### Using uv (Recommended for Development)

```bash
# Install uv if you haven't already
pip install uv

# Install fp-admin with all dependencies
uv sync --all-extras --dev

# Install git hooks
uv run pre-commit install
```

### From Source

```bash
# Clone the repository
git clone https://github.com/esmairi/fp-admin.git
cd fp-admin

# Install in development mode
pip install -e .[dev]

# Or using uv
uv sync --all-extras --dev
```

## Development Setup

### 1. Install Development Dependencies

```bash
# Using pip
pip install fp-admin[dev]

# Using uv
uv sync --all-extras --dev
```

### 2. Install Pre-commit Hooks

```bash
# Install git hooks for code quality
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

### 3. Set Up Testing Environment

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=fp_admin
```

## Database Setup

fp-admin supports multiple database backends:

### SQLite (Default)

No additional setup required. SQLite is included with Python.

### PostgreSQL

```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Or using uv
uv add psycopg2-binary
```

### MySQL

```bash
# Install MySQL adapter
pip install mysqlclient

# Or using uv
uv add mysqlclient
```

## Environment Variables

Create a `.env` file in your project root:

```bash
# Database
DATABASE_URL=sqlite:///./app.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin Settings
ADMIN_TITLE=fp-admin
ADMIN_DESCRIPTION=Modern FastAPI Admin Framework
```

## Verification

After installation, verify that fp-admin is working:

```bash
# Check if fp-admin is installed
fp-admin --version

# Create a test project
fp-admin startproject test-project
cd test-project

# Run the application
fp-admin run
```

Visit `http://localhost:8000/admin` to see the admin interface.

## Troubleshooting

### Common Issues

#### 1. Import Errors

If you encounter import errors, make sure you're using Python 3.12+:

```bash
python --version
```

#### 2. Database Connection Issues

Check your database URL format:

- SQLite: `sqlite:///./app.db`
- PostgreSQL: `postgresql://user:password@localhost/dbname`
- MySQL: `mysql://user:password@localhost/dbname`

#### 3. Permission Issues

On Linux/macOS, you might need to use `sudo` for global installations:

```bash
sudo pip install fp-admin
```

#### 4. Virtual Environment

It's recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/macOS
source venv/bin/activate

# Install fp-admin
pip install fp-admin
```

## Next Steps

After installation, proceed to:

- **[Quick Start](quick-start.md)** - Create your first admin interface
- **[Core Concepts](core-concepts.md)** - Understand the fundamental concepts
- **[User Guide](../user-guide/field-types.md)** - Learn about field types and widgets
