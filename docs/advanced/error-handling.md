# Error Handling in fp-admin

fp-admin provides a comprehensive error handling system that validates data before database operations and returns structured, field-specific error messages.

## Overview

The error handling system consists of two main components:

1. **ModelValidator** - Validates data before database operations
2. **ErrorHandler** - Handles database errors and converts them to structured responses

## Features

### Pre-Database Validation

The system validates model data before attempting database operations, catching errors early and providing better user experience:

- **Required field validation** - Checks for missing mandatory fields
- **Type validation** - Ensures correct data types (string, number, boolean)
- **Constraint validation** - Validates length limits, value ranges, patterns
- **Format validation** - Validates email formats, patterns, etc.

### Structured Error Responses

All errors are returned in a consistent, structured format:

```json
{
  "detail": {
    "error": {
      "password": ["password is mandatory"],
      "email": ["email format is invalid"],
      "username": ["username must be at least 3 characters long"]
    }
  }
}
```

### Database Error Handling

For errors that occur at the database level (e.g., unique constraint violations), the system parses SQLAlchemy errors and converts them to field-specific messages.

## Usage Examples

### API Endpoint Usage

When creating records via the API:

```bash
POST /api/v1/models/user
{
  "username": "testuser",
  "email": "invalid-email",
  "is_active": true
}
```

**Response (400 Bad Request):**
```json
{
  "detail": {
    "error": {
      "password": ["password is mandatory"],
      "email": ["email format is invalid"]
    }
  }
}
```

### Programmatic Usage

```python
from fp_admin.services.validator import ModelValidator
from fp_admin.apps.auth.models import User

# Validate data before database operations
data = {
    "username": "testuser",
    "email": "invalid-email",
    "password": "123"  # Too short
}

field_errors = ModelValidator.validate_model_data(User, data)
if field_errors:
    print("Validation errors:", field_errors)
```

## Error Types

### Validation Errors

These are caught before database operations:

- **Missing required fields** - `"field_name is mandatory"`
- **Invalid data types** - `"field_name must be a string/number/boolean"`
- **Length violations** - `"field_name must be at least X characters long"`
- **Value range violations** - `"field_name must be greater than X"`
- **Pattern violations** - `"field_name format is invalid"`

### Database Errors

These are caught during database operations:

- **NOT NULL constraint** - `"field_name is mandatory"`
- **UNIQUE constraint** - `"field_name must be unique"`
- **FOREIGN KEY constraint** - `"field_name references a non-existent record"`
- **CHECK constraint** - `"field_name value violates constraint"`

## Configuration

### Model Field Validation

Configure validation rules in your SQLModel fields:

```python
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    username: str = Field(unique=True, min_length=3, max_length=50)
    email: str = Field(unique=True, pattern=r"^[^@]+@[^@]+\.[^@]+$")
    password: str = Field(min_length=8)
    age: int = Field(gt=0, lt=150)
    score: float = Field(ge=0.0, le=100.0)
    is_active: bool = True
```

### Validation Rules

- **min_length/max_length** - String length constraints
- **gt/lt/gte/lte** - Numeric value constraints
- **pattern** - Regular expression pattern validation
- **unique** - Database unique constraint (validated at DB level)

## Testing

### Unit Tests

Test validation logic:

```python
def test_validate_required_fields():
    data = {"username": "testuser"}  # Missing password
    field_errors = ModelValidator.validate_model_data(User, data)
    assert "password" in field_errors
    assert "password is mandatory" in field_errors["password"]
```

### Integration Tests

Test API endpoints:

```python
def test_create_user_missing_password(client):
    response = client.post("/api/v1/models/user", json={
        "username": "testuser",
        "email": "test@example.com"
    })

    assert response.status_code == 400
    result = response.json()
    assert "password" in result["detail"]["error"]
```

## Best Practices

1. **Define clear validation rules** in your model fields
2. **Use descriptive error messages** that help users understand what went wrong
3. **Test both validation and database error scenarios**
4. **Handle errors gracefully** in your frontend applications
5. **Log validation errors** for debugging purposes

## Error Response Format

All error responses follow this consistent format:

```json
{
  "detail": {
    "error": {
      "field_name": ["error message"],
      "another_field": ["another error message"]
    }
  }
}
```

For general errors (not field-specific):

```json
{
  "detail": {
    "error": "General error message"
  }
}
```

## Migration Guide

If you're upgrading from a previous version:

1. **Update your model fields** to include validation rules
2. **Update your frontend** to handle the new error response format
3. **Test your API endpoints** to ensure they return structured errors
4. **Update your error handling** to use the new validation system

## Troubleshooting

### Common Issues

1. **Validation not working** - Ensure model fields have proper validation rules
2. **Error format inconsistent** - Check that you're using the latest API version
3. **Database errors not parsed** - Verify that the error handler is properly configured

### Debug Mode

Enable debug logging to see detailed validation information:

```python
import logging
logging.getLogger("fp_admin.services.validator").setLevel(logging.DEBUG)
```

## Contributing

When adding new validation rules:

1. **Update the ModelValidator** to handle new validation types
2. **Add unit tests** for the new validation logic
3. **Update documentation** to reflect new validation options
4. **Test with real models** to ensure compatibility
