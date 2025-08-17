# Models API

The Models API provides comprehensive CRUD operations for all registered models in fp-admin. This API is automatically generated based on your model configurations and provides consistent endpoints for data manipulation.

## Overview

The Models API is built on top of the services layer and provides:

- **Automatic CRUD endpoints** for all registered models
- **Form-based validation** using view configurations
- **Advanced filtering and pagination**
- **Relationship handling** for foreign keys and many-to-many fields
- **Comprehensive error handling** with detailed validation messages

## Base URL

```
/api/v1/models/{model_name}
```

Where `{model_name}` is the lowercase name of your model (e.g., `user`, `post`, `category`).

## Authentication

All endpoints require authentication. Include your JWT token in the Authorization header:

```http
Authorization: Bearer <your_access_token>
```

## Endpoints

### Create Record

**POST** `/api/v1/models/{model_name}`

Creates a new record for the specified model.

#### Request Body

```json
{
  "data": {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "is_active": true
  },
  "form_id": "UserForm"
}
```

#### Parameters

- `data` (object): The record data to create
- `form_id` (string, optional): Form configuration to use for validation

#### Response

```json
{
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Example

```bash
curl -X POST "http://localhost:8000/api/v1/models/user" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "username": "john_doe",
      "email": "john@example.com",
      "password": "SecurePass123!"
    },
    "form_id": "UserForm"
  }'
```

### List Records

**GET** `/api/v1/models/{model_name}`

Retrieves a paginated list of records for the specified model.

#### Query Parameters

- `page` (integer, default: 1): Page number
- `page_size` (integer, default: 20, max: 100): Number of records per page
- `fields` (string, optional): Comma-separated list of fields to include
- `filters` (string, optional): Filter criteria
- `sort_by` (string, optional): Field to sort by
- `sort_order` (string, optional): Sort order (asc/desc)

#### Response

```json
{
  "data": [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "username": "jane_smith",
      "email": "jane@example.com",
      "is_active": true,
      "created_at": "2024-01-15T11:00:00Z"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 20,
  "total_pages": 1,
  "has_next": false,
  "has_prev": false
}
```

#### Example

```bash
curl "http://localhost:8000/api/v1/models/user?page=1&page_size=10&fields=id,username,email" \
  -H "Authorization: Bearer <token>"
```

### Get Record by ID

**GET** `/api/v1/models/{model_name}/{record_id}`

Retrieves a single record by its ID.

#### Path Parameters

- `record_id` (integer): The ID of the record to retrieve

#### Response

```json
{
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Example

```bash
curl "http://localhost:8000/api/v1/models/user/1" \
  -H "Authorization: Bearer <token>"
```

### Update Record

**PUT** `/api/v1/models/{model_name}/{record_id}`

Updates an existing record.

#### Path Parameters

- `record_id` (integer): The ID of the record to update

#### Request Body

```json
{
  "data": {
    "email": "john.doe@example.com",
    "is_active": false
  },
  "form_id": "UserForm"
}
```

#### Response

```json
{
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john.doe@example.com",
    "is_active": false,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
  }
}
```

#### Example

```bash
curl -X PUT "http://localhost:8000/api/v1/models/user/1" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "email": "john.doe@example.com",
      "is_active": false
    },
    "form_id": "UserForm"
  }'
```

### Delete Record

**DELETE** `/api/v1/models/{model_name}/{record_id}`

Deletes a record.

#### Path Parameters

- `record_id` (integer): The ID of the record to delete

#### Response

```json
{
  "message": "Record deleted successfully"
}
```

#### Example

```bash
curl -X DELETE "http://localhost:8000/api/v1/models/user/1" \
  -H "Authorization: Bearer <token>"
```

## Advanced Features

### Filtering

The API supports advanced filtering using a simple syntax:

```bash
# Basic equality
?filters=is_active=true

# Multiple filters
?filters=is_active=true&filters=username__icontains=john

# Complex filters
?filters=created_at__gte=2024-01-01&filters=email__endswith=@gmail.com
```

#### Filter Operators

- `=` : Exact match
- `__icontains` : Contains (case-insensitive)
- `__startswith` : Starts with
- `__endswith` : Ends with
- `__gt` : Greater than
- `__gte` : Greater than or equal
- `__lt` : Less than
- `__lte` : Less than or equal
- `__in` : In list (comma-separated)

### Field Selection

Choose which fields to include in responses:

```bash
# Select specific fields
?fields=id,username,email

# Include relationship fields
?fields=id,username,groups&include=groups__name
```

### Sorting

Sort results by any field:

```bash
# Sort by field
?sort_by=username&sort_order=asc

# Sort by multiple fields
?sort_by=created_at,username&sort_order=desc,asc
```

## Error Handling

### Validation Errors

When form validation fails, the API returns detailed error messages:

```json
{
  "error": "Validation failed",
  "status_code": 422,
  "details": {
    "username": ["Username is required"],
    "email": ["Invalid email format"],
    "password": ["Password must be at least 8 characters"]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Responses

#### 400 Bad Request

```json
{
  "error": "Invalid request data",
  "status_code": 400,
  "details": "Missing required field: username"
}
```

#### 401 Unauthorized

```json
{
  "error": "Authentication required",
  "status_code": 401,
  "details": "Valid token required"
}
```

#### 403 Forbidden

```json
{
  "error": "Insufficient permissions",
  "status_code": 403,
  "details": "User does not have permission to access this resource"
}
```

#### 404 Not Found

```json
{
  "error": "Record not found",
  "status_code": 404,
  "details": "User with ID 999 does not exist"
}
```

#### 500 Internal Server Error

```json
{
  "error": "Internal server error",
  "status_code": 500,
  "details": "Database connection failed"
}
```

## Rate Limiting

The API includes rate limiting to prevent abuse:

- **Default**: 100 requests per minute per user
- **Authentication endpoints**: 5 requests per minute per IP
- **File uploads**: 10 requests per minute per user

Rate limit headers are included in responses:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642233600
```

## Pagination

All list endpoints support pagination with the following response structure:

```json
{
  "data": [...],
  "total": 150,
  "page": 2,
  "page_size": 20,
  "total_pages": 8,
  "has_next": true,
  "has_prev": true
}
```

### Pagination Parameters

- `page`: Current page number (1-based)
- `page_size`: Number of items per page (1-100)
- `total`: Total number of items
- `total_pages`: Total number of pages
- `has_next`: Whether there's a next page
- `has_prev`: Whether there's a previous page

## Relationship Handling

### Foreign Key Relationships

The API automatically handles foreign key relationships:

```json
{
  "data": {
    "id": 1,
    "title": "My First Post",
    "author_id": 5,
    "author": {
      "id": 5,
      "username": "john_doe",
      "email": "john@example.com"
    }
  }
}
```

### Many-to-Many Relationships

Many-to-many relationships are also supported:

```json
{
  "data": {
    "id": 1,
    "title": "My First Post",
    "tags": [
      {"id": 1, "name": "python"},
      {"id": 2, "name": "fastapi"}
    ]
  }
}
```

## Bulk Operations

### Bulk Create

**POST** `/api/v1/models/{model_name}/bulk`

Creates multiple records at once:

```json
{
  "records": [
    {
      "username": "user1",
      "email": "user1@example.com"
    },
    {
      "username": "user2",
      "email": "user2@example.com"
    }
  ],
  "form_id": "UserForm"
}
```

### Bulk Update

**PUT** `/api/v1/models/{model_name}/bulk`

Updates multiple records:

```json
{
  "updates": [
    {"id": 1, "data": {"is_active": false}},
    {"id": 2, "data": {"is_active": true}}
  ],
  "form_id": "UserForm"
}
```

### Bulk Delete

**DELETE** `/api/v1/models/{model_name}/bulk`

Deletes multiple records:

```json
{
  "ids": [1, 2, 3]
}
```

## Search

### Full-Text Search

**GET** `/api/v1/models/{model_name}/search?q={query}`

Performs full-text search across searchable fields:

```bash
curl "http://localhost:8000/api/v1/models/user/search?q=john" \
  -H "Authorization: Bearer <token>"
```

### Search Parameters

- `q` (string): Search query
- `fields` (string, optional): Fields to search in
- `fuzzy` (boolean, optional): Enable fuzzy matching

## Export

### Export to CSV

**GET** `/api/v1/models/{model_name}/export?format=csv`

Exports data in CSV format:

```bash
curl "http://localhost:8000/api/v1/models/user/export?format=csv" \
  -H "Authorization: Bearer <token>" \
  -o users.csv
```

### Export to JSON

**GET** `/api/v1/models/{model_name}/export?format=json`

Exports data in JSON format:

```bash
curl "http://localhost:8000/api/v1/models/user/export?format=json" \
  -H "Authorization: Bearer <token>" \
  -o users.json
```

## Webhooks

### Webhook Configuration

Configure webhooks for model events:

```json
{
  "webhooks": [
    {
      "url": "https://your-app.com/webhooks/user-created",
      "events": ["create", "update", "delete"],
      "secret": "webhook-secret"
    }
  ]
}
```

### Webhook Events

- `create`: Record created
- `update`: Record updated
- `delete`: Record deleted

### Webhook Payload

```json
{
  "event": "create",
  "model": "user",
  "data": {
    "id": 1,
    "username": "john_doe"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "signature": "sha256=..."
}
```

## Testing

### Test Endpoints

Use the test endpoints for development and testing:

```bash
# Test endpoint (no authentication required)
curl "http://localhost:8000/api/v1/models/user/test"

# Test with sample data
curl "http://localhost:8000/api/v1/models/user/test?sample=true"
```

### Mock Data

Generate mock data for testing:

```bash
# Generate 10 mock users
curl "http://localhost:8000/api/v1/models/user/mock?count=10" \
  -H "Authorization: Bearer <token>"
```

## Best Practices

### 1. Use Form Validation

Always specify a `form_id` for proper validation:

```json
{
  "data": {...},
  "form_id": "UserForm"
}
```

### 2. Handle Errors Gracefully

Implement proper error handling in your client:

```python
try:
    response = await api.create_user(user_data)
    return response["data"]
except ValidationError as e:
    # Handle validation errors
    for field, errors in e.details.items():
        print(f"{field}: {errors}")
except APIError as e:
    # Handle other API errors
    print(f"API Error: {e.message}")
```

### 3. Use Pagination

Always implement pagination for large datasets:

```python
page = 1
all_users = []

while True:
    response = await api.get_users(page=page, page_size=100)
    users = response["data"]
    all_users.extend(users)

    if not response["has_next"]:
        break

    page += 1
```

### 4. Optimize Field Selection

Only request the fields you need:

```python
# Instead of getting all fields
users = await api.get_users()

# Request only needed fields
users = await api.get_users(fields="id,username,email")
```

## Next Steps

- **[Views API](views.md)** - Admin view configuration API
- **[Apps API](apps.md)** - Application management API
- **[Services Layer](../user-guide/services.md)** - Business logic services
- **[Authentication](../user-guide/authentication.md)** - User authentication
