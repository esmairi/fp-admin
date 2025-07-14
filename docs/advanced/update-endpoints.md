# Update Record Endpoint

The update record endpoint allows you to update existing records in the fp-admin system.

## Endpoint

```
PUT /api/v1/models/{model_name}/{record_id}
```

## Request Format

The request body should follow the same format as the create endpoint:

```json
{
  "data": {
    "field1": "value1",
    "field2": "value2"
  },
  "form_id": "optional_form_id"
}
```

### Parameters

- `model_name` (path): The name of the model to update
- `record_id` (path): The ID of the record to update
- `data` (body): The fields to update
- `form_id` (body, optional): Form ID for validation

## Response Format

```json
{
  "data": {
    "id": 1,
    "field1": "updated_value1",
    "field2": "updated_value2"
  }
}
```

## Features

### Form Validation

If a `form_id` is provided, the update will be validated using the form's validation rules:

```json
{
  "data": {
    "username": "new_username",
    "email": "new@example.com"
  },
  "form_id": "user_form"
}
```

**Important**: During updates, form validation has access to **all fields** from the existing record, not just the fields being updated. This is crucial for cross-field validation rules.

For example, if you have a form validation rule that prevents `email` from being equal to `username`, and you only update the `email` field:

```json
{
  "data": {
    "email": "testuser@example.com"  // Only updating email
  },
  "form_id": "user_form"
}
```

The form validation will receive both the existing `username` value and the new `email` value, allowing it to perform cross-field validation correctly.

**Implementation Details**: The system automatically merges the existing record data with the update data before validation, ensuring form validation has complete context.

### Error Handling

The endpoint returns appropriate error responses:

- **400 Bad Request**: If the model doesn't exist or the record is not found
- **400 Bad Request**: If validation fails (with detailed field errors)
- **400 Bad Request**: If non-allowed fields are being updated
- **500 Internal Server Error**: For other server errors

### Allowed Update Fields

You can restrict which fields can be updated by setting `allowed_update_fields` in your view builder:

```python
class UserFormView(BaseViewBuilder):
    name = "user_form"
    model = User
    view_type = "form"
    fields = [
        TextField(name="username", label="Username"),
        EmailField(name="email", label="Email"),
        BooleanField(name="is_active", label="Active"),
        BooleanField(name="is_superuser", label="Superuser"),
    ]

    # Only allow creating username, email, and password fields
    creation_fields = ["username", "email", "password"]

    # Only allow updating email and is_active fields
    allowed_update_fields = ["email", "is_active"]
```

When `allowed_update_fields` is configured, the update endpoint will validate that only allowed fields are being updated. If non-allowed fields are included in the update request, the endpoint will return a 400 error with field-specific error messages.

**Example Error Response:**
```json
{
  "detail": {
    "error": {
      "username": ["Field 'username' is not allowed to be updated"],
      "is_superuser": ["Field 'is_superuser' is not allowed to be updated"]
    }
  }
}
```

### Creation Fields

Similarly, you can restrict which fields can be used during creation by setting `creation_fields`:

```python
class UserFormView(BaseViewBuilder):
    # ... other configuration ...

    # Only allow creating username, email, and password fields
    creation_fields = ["username", "email", "password"]
```

This prevents users from setting fields like `is_superuser` or `is_active` during creation, even if they're defined in the form.

### Field References Validation

The system automatically validates that all fields referenced in `creation_fields` and `allowed_update_fields` actually exist in the view's `fields` list. This validation happens at class definition time, so configuration errors are caught early.

**Example of valid configuration:**
```python
class UserFormView(BaseViewBuilder):
    name = "user_form"
    model = User
    view_type = "form"
    fields = [
        TextField(name="username", label="Username"),
        EmailField(name="email", label="Email"),
        BooleanField(name="is_active", label="Active"),
    ]

    # All these fields exist in the fields list above
    creation_fields = ["username", "email"]
    allowed_update_fields = ["email", "is_active"]
```

**Example of invalid configuration (will raise ValueError):**
```python
class InvalidUserFormView(BaseViewBuilder):
    name = "invalid_user_form"
    model = User
    view_type = "form"
    fields = [
        TextField(name="username", label="Username"),
        EmailField(name="email", label="Email"),
    ]

    # These fields don't exist in the fields list above
    creation_fields = ["username", "email", "nonexistent_field"]  # ❌ Error
    allowed_update_fields = ["email", "missing_field"]  # ❌ Error
```

The validation error will clearly indicate which fields are missing:
```
ValueError: Fields referenced in creation_fields do not exist in the view's fields: ['nonexistent_field']
```

This ensures that your view configurations are always consistent and prevents runtime errors from misconfigured field references.

### Example Usage

#### Update a user record:

```bash
curl -X PUT "http://localhost:8000/api/v1/models/user/1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "username": "updated_username",
      "email": "updated@example.com",
      "is_active": false
    }
  }'
```

#### Update with form validation:

```bash
curl -X PUT "http://localhost:8000/api/v1/models/user/1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "username": "updated_username",
      "email": "updated@example.com"
    },
    "form_id": "user_form"
  }'
```

## Implementation Details

The update endpoint:

1. **Validates the model exists** in the registry
2. **Validates allowed creation fields** (if configured in view builder)
3. **Validates allowed update fields** (if configured in view builder)
4. **Retrieves the existing record** by ID (if form validation is needed)
5. **Merges existing data with update data** for form validation (ensuring cross-field validation works)
6. **Applies form validation** if `form_id` is provided (with complete field context)
7. **Updates the record fields** with the provided data
8. **Saves the changes and serializes** the record inside the database session for data consistency
9. **Returns the updated record** in the response

The endpoint follows the same patterns as the create endpoint for consistency and reuses the existing validation and error handling infrastructure. **Importantly, the serialization happens inside the database session to ensure data consistency and prevent race conditions.**

**Key Features:**
- **Creation Fields**: Restrict which fields can be used during creation via `creation_fields` in view builders
- **Allowed Update Fields**: Restrict which fields can be updated via `allowed_update_fields` in view builders
- **Cross-field Validation**: During updates, form validation receives the complete record data (existing + updated fields) rather than just the fields being updated, enabling proper cross-field validation
- **Field Name Approach**: Uses simple field names (strings) instead of FieldView objects for better simplicity and flexibility
