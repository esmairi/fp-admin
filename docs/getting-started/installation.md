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

fp-admin uses **async database operations** by default, providing better performance and scalability. The framework supports multiple async database backends:

### SQLite (Default - Async)

fp-admin uses `aiosqlite` for async SQLite operations:

```bash
# No additional setup required for SQLite
# aiosqlite is included in fp-admin dependencies
```

**Default Database URL**: `sqlite+aiosqlite:///./fpadmin.db`

### PostgreSQL (Async)

For PostgreSQL, use the async adapter:

```bash
# Install async PostgreSQL adapter
pip install asyncpg

# Or using uv
uv add asyncpg
```

**Database URL Format**: `postgresql+asyncpg://user:password@localhost/dbname`

### MySQL (Async)

For MySQL, use the async adapter:

```bash
# Install async MySQL adapter
pip install aiomysql

# Or using uv
uv add aiomysql
```

**Database URL Format**: `mysql+aiomysql://user:password@localhost/dbname`

### Async Database Benefits

- **Non-blocking I/O**: Database operations don't block the event loop
- **Better concurrency**: Handle multiple requests simultaneously
- **Scalability**: Improved performance under high load
- **Modern architecture**: Built for async/await patterns

### Async Database Configuration

fp-admin automatically handles async database connections. Your models and services will work with async/await patterns:

```python
from fp_admin.core.db import db_manager
from sqlmodel.ext.asyncio.session import AsyncSession

async def example_operation():
    async with db_manager.get_session() as session:
        # All database operations are async
        result = await session.exec(select(User))
        users = result.all()
        return users
```

## Environment Variables

Create a `.env` file in your project root:

```bash
# Database (Async)
DATABASE_URL=sqlite+aiosqlite:///./fpadmin.db
# For PostgreSQL: postgresql+asyncpg://user:password@localhost/dbname
# For MySQL: mysql+aiomysql://user:password@localhost/dbname

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

Check your database URL format for async operations:

- **SQLite (Async)**: `sqlite+aiosqlite:///./fpadmin.db`
- **PostgreSQL (Async)**: `postgresql+asyncpg://user:password@localhost/dbname`
- **MySQL (Async)**: `mysql+aiomysql://user:password@localhost/dbname`

**Note**: Make sure you're using the async database adapters (`aiosqlite`, `asyncpg`, `aiomysql`) for optimal performance.

#### 2.1. Async Database Specific Issues

If you encounter async-related errors:

```bash
# Make sure you have the correct async adapters
pip install aiosqlite asyncpg aiomysql

# Check if your code uses async/await patterns
# Database operations should be awaited:
# result = await session.exec(query)  # ✅ Correct
# result = session.exec(query)        # ❌ Wrong
```

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

## Async Development Best Practices

When working with fp-admin's async database:

1. **Always use async/await**: Database operations must be awaited
2. **Use async context managers**: `async with db_manager.get_session() as session:`
3. **Handle async errors properly**: Use try/catch with async operations
4. **Avoid blocking operations**: Keep database operations non-blocking

## Next Steps

After installation, proceed to:

- **[Quick Start](quick-start.md)** - Create your first admin interface
- **[Core Concepts](core-concepts.md)** - Understand the fundamental concepts
- **[Configuration](../configuration/settings.md)** - Configure your application settings
- **[User Guide](../user-guide/field-types.md)** - Learn about field types and widgets
