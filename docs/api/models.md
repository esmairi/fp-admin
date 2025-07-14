# Models API

This guide covers the REST API endpoints for model CRUD operations in fp-admin.

## Overview

fp-admin automatically generates REST API endpoints for all registered models. These endpoints provide full CRUD (Create, Read, Update, Delete) operations with filtering, pagination, and field selection.

## Base URL

All API endpoints are prefixed with `/api/v1/models/`:

```
https://your-domain.com/api/v1/models/{model_name}/
```

## Authentication

All API endpoints require authentication. Include the JWT token in the Authorization header:

```bash
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### List Records

**GET** `/api/v1/models/{model_name}/`

Retrieve a list of records with optional filtering, pagination, and field selection.

#### Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `page` | integer | Page number (default: 1) | `?page=2` |
| `page_size` | integer | Records per page (default: 20, max: 100) | `?page_size=50` |
| `search` | string | Search across searchable fields | `?search=john` |
| `ordering` | string | Sort by field (prefix with `-` for descending) | `?ordering=-created_at` |
| `fields` | string | Comma-separated list of fields to include | `?fields=id,name,email` |
| `exclude` | string | Comma-separated list of fields to exclude | `?exclude=password,secret` |

#### Query Parameters

**Filtering:**
```bash
# Filter by exact match
?field=value

# Filter by multiple values
?field__in=value1,value2,value3

# Filter by range
?field__gte=value&field__lte=value

# Filter by contains
?field__contains=value

# Filter by starts with
?field__startswith=value

# Filter by ends with
?field__endswith=value

# Filter by null/not null
?field__isnull=true
?field__isnull=false
```

**Search:**
```bash
# Search across multiple fields
?search=john

# Search in specific field
?name__icontains=john
?email__icontains=john
```

**Ordering:**
```bash
# Single field ordering
?ordering=name

# Descending order
?ordering=-created_at

# Multiple field ordering
?ordering=category,name
```

#### Example Requests

```bash
# Get all users
GET /api/v1/models/user/

# Get users with pagination
GET /api/v1/models/user/?page=1&page_size=20

# Search for users
GET /api/v1/models/user/?search=john

# Filter active users
GET /api/v1/models/user/?is_active=true

# Order by creation date
GET /api/v1/models/user/?ordering=-created_at

# Select specific fields
GET /api/v1/models/user/?fields=id,username,email,created_at

# Complex filtering
GET /api/v1/models/user/?is_active=true&created_at__gte=2023-01-01&ordering=-created_at
```

#### Response Format

```json
{
  "count": 100,
  "next": "https://api.example.com/api/v1/models/user/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "is_active": true,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "username": "jane_smith",
      "email": "jane@example.com",
      "is_active": true,
      "created_at": "2023-01-02T00:00:00Z",
      "updated_at": "2023-01-02T00:00:00Z"
    }
  ]
}
```

### Create Record

**POST** `/api/v1/models/{model_name}/`

Create a new record.

#### Request Body

The request body should contain the field values for the new record:

```json
{
  "username": "new_user",
  "email": "newuser@example.com",
  "password": "secure_password",
  "is_active": true
}
```

#### Example Request

```bash
curl -X POST /api/v1/models/user/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "new_user",
    "email": "newuser@example.com",
    "password": "secure_password",
    "is_active": true
  }'
```

#### Response Format

```json
{
  "id": 3,
  "username": "new_user",
  "email": "newuser@example.com",
  "is_active": true,
  "created_at": "2023-01-03T00:00:00Z",
  "updated_at": "2023-01-03T00:00:00Z"
}
```

### Get Record

**GET** `/api/v1/models/{model_name}/{id}/`

Retrieve a specific record by ID.

#### Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `fields` | string | Comma-separated list of fields to include | `?fields=id,name,email` |
| `exclude` | string | Comma-separated list of fields to exclude | `?exclude=password,secret` |

#### Example Request

```bash
# Get user by ID
GET /api/v1/models/user/1/

# Get user with specific fields
GET /api/v1/models/user/1/?fields=id,username,email
```

#### Response Format

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Update Record

**PUT** `/api/v1/models/{model_name}/{id}/`

Update an existing record (full update - all fields required).

#### Request Body

```json
{
  "username": "updated_user",
  "email": "updated@example.com",
  "is_active": false
}
```

#### Example Request

```bash
curl -X PUT /api/v1/models/user/1/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "updated_user",
    "email": "updated@example.com",
    "is_active": false
  }'
```

#### Response Format

```json
{
  "id": 1,
  "username": "updated_user",
  "email": "updated@example.com",
  "is_active": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-03T00:00:00Z"
}
```

### Partial Update Record

**PATCH** `/api/v1/models/{model_name}/{id}/`

Partially update an existing record (only specified fields).

#### Request Body

```json
{
  "email": "newemail@example.com",
  "is_active": false
}
```

#### Example Request

```bash
curl -X PATCH /api/v1/models/user/1/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com",
    "is_active": false
  }'
```

#### Response Format

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "newemail@example.com",
  "is_active": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-03T00:00:00Z"
}
```

### Delete Record

**DELETE** `/api/v1/models/{model_name}/{id}/`

Delete a specific record.

#### Example Request

```bash
curl -X DELETE /api/v1/models/user/1/ \
  -H "Authorization: Bearer <token>"
```

#### Response Format

```json
{
  "message": "Record deleted successfully"
}
```

## Field Types and Validation

### String Fields

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Validation:**
- Required fields must be provided
- String length limits are enforced
- Email format validation for email fields
- Unique constraints are enforced

### Number Fields

```json
{
  "age": 25,
  "price": 99.99,
  "rating": 4.5
}
```

**Validation:**
- Min/max value constraints
- Integer vs float validation
- Range validation

### Boolean Fields

```json
{
  "is_active": true,
  "is_verified": false,
  "is_superuser": false
}
```

### Date/Time Fields

```json
{
  "birth_date": "1990-01-01",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Foreign Key Fields

```json
{
  "author_id": 1,
  "category_id": 2,
  "parent_id": null
}
```

### Many-to-Many Fields

```json
{
  "tags": [1, 2, 3],
  "permissions": [1, 2, 3, 4]
}
```

## Error Handling

### Validation Errors

When validation fails, the API returns a 400 status code with detailed error messages:

```json
{
  "detail": "Validation failed",
  "errors": {
    "username": [
      "This field is required."
    ],
    "email": [
      "Enter a valid email address."
    ],
    "age": [
      "Ensure this value is greater than or equal to 0."
    ]
  }
}
```

### Not Found Errors

When a record is not found:

```json
{
  "detail": "Record not found"
}
```

### Permission Errors

When the user doesn't have permission:

```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Authentication Errors

When authentication fails:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

## Pagination

The API uses cursor-based pagination with the following response format:

```json
{
  "count": 100,
  "next": "https://api.example.com/api/v1/models/user/?cursor=abc123",
  "previous": null,
  "results": [...]
}
```

### Pagination Parameters

- `page`: Page number (default: 1)
- `page_size`: Records per page (default: 20, max: 100)

## Filtering

### Exact Match

```bash
GET /api/v1/models/user/?is_active=true
GET /api/v1/models/user/?username=john_doe
```

### Contains

```bash
GET /api/v1/models/user/?username__contains=john
GET /api/v1/models/user/?email__contains=example
```

### Starts/Ends With

```bash
GET /api/v1/models/user/?username__startswith=john
GET /api/v1/models/user/?email__endswith=@example.com
```

### Greater/Less Than

```bash
GET /api/v1/models/user/?created_at__gte=2023-01-01
GET /api/v1/models/user/?age__lte=30
```

### In List

```bash
GET /api/v1/models/user/?id__in=1,2,3,4,5
GET /api/v1/models/user/?status__in=active,inactive
```

### Null/Not Null

```bash
GET /api/v1/models/user/?deleted_at__isnull=true
GET /api/v1/models/user/?email__isnull=false
```

## Search

### Global Search

Search across all searchable fields:

```bash
GET /api/v1/models/user/?search=john
```

### Field-Specific Search

```bash
GET /api/v1/models/user/?username__icontains=john
GET /api/v1/models/user/?email__icontains=example
```

## Ordering

### Single Field

```bash
GET /api/v1/models/user/?ordering=username
GET /api/v1/models/user/?ordering=-created_at
```

### Multiple Fields

```bash
GET /api/v1/models/user/?ordering=is_active,-created_at,username
```

## Field Selection

### Include Specific Fields

```bash
GET /api/v1/models/user/?fields=id,username,email
```

### Exclude Specific Fields

```bash
GET /api/v1/models/user/?exclude=password,secret_key
```

## Examples

### User Management

```bash
# List all users
GET /api/v1/models/user/

# Create new user
POST /api/v1/models/user/
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "secure123",
  "is_active": true
}

# Get specific user
GET /api/v1/models/user/1/

# Update user
PUT /api/v1/models/user/1/
{
  "username": "updateduser",
  "email": "updated@example.com",
  "is_active": false
}

# Delete user
DELETE /api/v1/models/user/1/
```

### Blog Posts

```bash
# List posts with filtering
GET /api/v1/models/post/?is_published=true&ordering=-created_at

# Create new post
POST /api/v1/models/post/
{
  "title": "My First Post",
  "content": "This is the content of my first post.",
  "author_id": 1,
  "category_id": 2,
  "tags": [1, 2, 3],
  "is_published": true
}

# Get post with related data
GET /api/v1/models/post/1/?fields=id,title,content,author,created_at
```

### Complex Queries

```bash
# Advanced filtering and search
GET /api/v1/models/post/?search=python&is_published=true&created_at__gte=2023-01-01&ordering=-created_at&page=1&page_size=10

# Multiple field selection
GET /api/v1/models/user/?fields=id,username,email,created_at&exclude=password,secret_key
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Anonymous users**: 100 requests per hour
- **Authenticated users**: 1000 requests per hour
- **Premium users**: 10000 requests per hour

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Caching

The API supports caching with ETags and Last-Modified headers:

```
ETag: "abc123"
Last-Modified: Wed, 01 Jan 2023 00:00:00 GMT
```

## Next Steps

- **[Views API](views.md)** - Admin view configuration API
- **[Apps API](apps.md)** - Application management API
- **[Authentication](../user-guide/authentication.md)** - User management and authentication
