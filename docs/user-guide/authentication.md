# Authentication (TODO)

This guide covers authentication and user management in fp-admin.

## Overview

fp-admin includes a complete authentication system with user management, role-based access control, and JWT token authentication.

## User Model

The default user model includes:

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True, table_name="user"):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(title="Username", nullable=False, unique=True, max_length=150)
    email: str = Field(
        title="Email",
        nullable=False,
        unique=True,
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    )
    password: str = Field(title="Password", nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)

    groups: List["Group"] = Relationship(back_populates="users", link_model=UserGroupLink)
```

## Authentication Views

### User Admin View

```python
from fp_admin.admin.views import BaseViewBuilder
from fp_admin.admin.fields import FieldFactory
from .models import User, Group

class UserFormView(BaseViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("username", "Username", required=True),
        FieldFactory.email_field("email", "Email", required=True),
        FieldFactory.password_field("password", "Password", required=True, min_length=8),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),
        FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name"),
    ]

    creation_fields = ["username", "email", "password", "is_active", "is_superuser"]
    allowed_update_fields = ["email", "is_active", "is_superuser"]

class UserListView(BaseViewBuilder):
    model = User
    view_type = "list"
    name = "UserList"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("username", "Username"),
        FieldFactory.email_field("email", "Email"),
        FieldFactory.boolean_field("is_active", "Active"),
        FieldFactory.boolean_field("is_superuser", "Superuser"),
    ]
```

### Group Admin View

```python
from .models import Group, Permission, User

class GroupFormView(BaseViewBuilder):
    model = Group
    view_type = "form"
    name = "GroupForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("name", "Name", required=True, min_length=1),
        FieldFactory.string_field("description", "Description", required=True, min_length=1, max_length=200),
        FieldFactory.many_to_many_field("permissions", "Permissions", model_class=Permission, field_title="name"),
        FieldFactory.many_to_many_field("users", "Users", model_class=User, field_title="username"),
    ]

    creation_fields = ["name", "description"]
    allowed_update_fields = ["name", "description", "permissions"]

class GroupListView(BaseViewBuilder):
    model = Group
    view_type = "list"
    name = "GroupList"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("name", "Name"),
        FieldFactory.string_field("description", "Description"),
    ]
```

### Permission Admin View

```python
from .models import Permission, Group

class PermissionFormView(BaseViewBuilder):
    model = Permission
    view_type = "form"
    name = "PermissionForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("codename", "Code Name", required=True, min_length=1, max_length=150),
        FieldFactory.string_field("name", "Name", required=True, min_length=1, max_length=150),
        FieldFactory.string_field("description", "Description", required=True, min_length=1, max_length=200),
        FieldFactory.many_to_many_field("groups", "Groups", model_class=Group, field_title="name"),
    ]

    creation_fields = ["codename", "name", "description"]
    allowed_update_fields = ["codename", "name", "description"]

class PermissionListView(BaseViewBuilder):
    model = Permission
    view_type = "list"
    name = "PermissionList"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("codename", "Code Name"),
        FieldFactory.string_field("name", "Name"),
        FieldFactory.string_field("description", "Description"),
    ]
```

## Authentication Configuration

### Settings

```python
# settings.py
from fp_admin.global_settings import *

# Authentication settings
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password settings
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGITS = True
PASSWORD_REQUIRE_SPECIAL = True

# Session settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
```

### JWT Configuration

```python
# JWT settings
JWT_SECRET_KEY = "your-jwt-secret-key"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7

# JWT token types
JWT_TOKEN_TYPE_ACCESS = "access"
JWT_TOKEN_TYPE_REFRESH = "refresh"
```

## Authentication Endpoints

### Login

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fp_admin.apps.auth.services import AuthService

router = APIRouter()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return access token"""
    auth_service = AuthService()
    user = auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="INVALID CREDENTIALS")

    if not user.is_active:
        raise HTTPException(status_code=401, detail="USER IS INACTIVE")

    access_token = auth_service.create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
        }
    }
```

### Register

```python
@router.post("/register")
async def register(user_data: UserCreate):
    """Register a new user"""
    auth_service = AuthService()

    # Check if user already exists
    if auth_service.get_user_by_username(user_data.username):
        raise HTTPException(status_code=400, detail="USERNAME ALREADY REGISTERED")

    if auth_service.get_user_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="EMAIL ALREADY REGISTERED")

    # Create new user
    user = auth_service.create_user(user_data)

    return {
        "message": "USER CREATED SUCCESSFULLY",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    }
```

### Logout

```python
@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout current user"""
    # In a real implementation, you might want to blacklist the token
    return {"message": "LOGOUT SUCCESSFUL"}
```

### Refresh Token

```python
@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """Refresh access token"""
    auth_service = AuthService()

    try:
        payload = auth_service.verify_token(refresh_token)
        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=401, detail="INVALID TOKEN")

        user = auth_service.get_user_by_username(username)
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="USER NOT FOUND OR INACTIVE")

        new_access_token = auth_service.create_access_token(data={"sub": username})

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except Exception:
        raise HTTPException(status_code=401, detail="INVALID REFRESH TOKEN")
```

## User Management

### Create User

```python
from fp_admin.apps.auth.models import User
from fp_admin.apps.auth.services import AuthService

def create_user(username: str, email: str, password: str, **kwargs):
    """Create a new user"""
    auth_service = AuthService()

    user_data = {
        "username": username,
        "email": email,
        "password": password,
        **kwargs
    }

    return auth_service.create_user(user_data)
```

### Update User

```python
def update_user(user_id: int, **kwargs):
    """Update user information"""
    auth_service = AuthService()

    user = auth_service.get_user_by_id(user_id)
    if not user:
        raise ValueError("USER NOT FOUND")

    return auth_service.update_user(user, kwargs)
```

### Delete User

```python
def delete_user(user_id: int):
    """Delete a user"""
    auth_service = AuthService()

    user = auth_service.get_user_by_id(user_id)
    if not user:
        raise ValueError("USER NOT FOUND")

    return auth_service.delete_user(user)
```

## Group Management

### Create Group

```python
from fp_admin.apps.auth.models import Group

def create_group(name: str, description: str = ""):
    """Create a new group"""
    group = Group(name=name, description=description)
    # Save to database
    return group
```

### Add User to Group

```python
def add_user_to_group(user_id: int, group_id: int):
    """Add a user to a group"""
    user = get_user_by_id(user_id)
    group = get_group_by_id(group_id)

    if user and group:
        user.groups.append(group)
        # Save to database
        return True
    return False
```

### Remove User from Group

```python
def remove_user_from_group(user_id: int, group_id: int):
    """Remove a user from a group"""
    user = get_user_by_id(user_id)
    group = get_group_by_id(group_id)

    if user and group and group in user.groups:
        user.groups.remove(group)
        # Save to database
        return True
    return False
```

## Permission Management

### Create Permission

```python
from fp_admin.apps.auth.models import Permission

def create_permission(codename: str, name: str, description: str = ""):
    """Create a new permission"""
    permission = Permission(
        codename=codename,
        name=name,
        description=description
    )
    # Save to database
    return permission
```

### Add Permission to Group

```python
def add_permission_to_group(permission_id: int, group_id: int):
    """Add a permission to a group"""
    permission = get_permission_by_id(permission_id)
    group = get_group_by_id(group_id)

    if permission and group:
        group.permissions.append(permission)
        # Save to database
        return True
    return False
```

### Check User Permissions

```python
def has_permission(user: User, permission_codename: str):
    """Check if user has a specific permission"""
    for group in user.groups:
        for permission in group.permissions:
            if permission.codename == permission_codename:
                return True
    return False
```

## Security Best Practices

### Password Validation

```python
def validate_password(password: str) -> bool:
    """Validate password strength"""
    if len(password) < 8:
        return False

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    return has_upper and has_lower and has_digit and has_special
```

### Token Security

```python
def create_secure_token(user_id: int, expires_delta: timedelta = None):
    """Create a secure JWT token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Rate Limiting

```python
from fastapi import HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with rate limiting"""
    # ... login logic
```

## Error Handling

### Custom Authentication Exceptions

```python
class AuthenticationError(Exception):
    """Custom authentication error"""
    pass

class UserNotFoundError(AuthenticationError):
    """User not found error"""
    pass

class InvalidCredentialsError(AuthenticationError):
    """Invalid credentials error"""
    pass

class UserInactiveError(AuthenticationError):
    """User inactive error"""
    pass
```

### Error Response Format

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

@router.exception_handler(AuthenticationError)
async def authentication_exception_handler(request, exc):
    """Handle authentication errors"""
    return JSONResponse(
        status_code=401,
        content={
            "error": "AUTHENTICATION ERROR",
            "detail": str(exc),
            "type": exc.__class__.__name__
        }
    )
```

## Testing Authentication

### Test User Creation

```python
import pytest
from fp_admin.apps.auth.models import User
from fp_admin.apps.auth.services import AuthService

def test_create_user():
    """Test user creation"""
    auth_service = AuthService()

    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!"
    }

    user = auth_service.create_user(user_data)

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.is_active is True
```

### Test Authentication

```python
def test_user_authentication():
    """Test user authentication"""
    auth_service = AuthService()

    # Create user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!"
    }
    user = auth_service.create_user(user_data)

    # Test authentication
    authenticated_user = auth_service.authenticate_user("testuser", "SecurePass123!")

    assert authenticated_user is not None
    assert authenticated_user.id == user.id
```

### Test Permission Checking

```python
def test_user_permissions():
    """Test user permission checking"""
    # Create user, group, and permission
    user = create_user("testuser", "test@example.com", "password")
    group = create_group("testgroup")
    permission = create_permission("test_permission", "Test Permission")

    # Add user to group and permission to group
    add_user_to_group(user.id, group.id)
    add_permission_to_group(permission.id, group.id)

    # Test permission checking
    assert has_permission(user, "test_permission") is True
    assert has_permission(user, "non_existent_permission") is False
```
