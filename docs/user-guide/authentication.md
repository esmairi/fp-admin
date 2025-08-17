# Authentication

fp-admin provides a comprehensive authentication system with support for multiple authentication providers, JWT tokens, and role-based access control.

## Overview

The authentication system is built around the concept of **providers** - modular components that handle different authentication methods:

- **Internal Provider**: Username/password authentication with JWT tokens
- **OAuth Providers**: External OAuth service integration (planned)
- **Custom Providers**: Extensible provider system for custom authentication

## Quick Start

### 1. Basic Authentication Setup

```python
# settings.py
from fp_admin.global_settings import Settings

class MySettings(Settings):
    SECRET_KEY = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_MINUTES = 90
    DATABASE_URL = "sqlite+aiosqlite:///./app.db"

# main.py
from fp_admin import FastAPIAdmin
from fp_admin.apps.auth import *  # Import auth models and views

app = FastAPIAdmin()
```

### 2. Create Authentication Endpoints

```python
# apps/auth/routers.py
from fastapi import APIRouter, Depends
from fp_admin.core import get_session
from .schemas import SigninRequest, SignupRequest
from .services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
async def signup(request: SignupRequest, session=Depends(get_session)):
    user_service = UserService(session)
    return await user_service.create_user(request.data)

@router.post("/signin")
async def signin(request: SigninRequest, session=Depends(get_session)):
    user_service = UserService(session)
    return await user_service.authenticate_and_issue_token(
        request.data.username,
        request.data.password
    )
```

## Authentication Models

### User Model

The default User model includes comprehensive user management features:

```python
from fp_admin.apps.auth.models import User, Group, Permission

class User(TimestampedModel, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=150)
    email: str = Field(unique=True, max_length=255)
    password: str = Field(max_length=255)
    first_name: Optional[str] = Field(max_length=100)
    last_name: Optional[str] = Field(max_length=100)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    email_verified: bool = Field(default=False)
    last_login: Optional[datetime] = None

    # Relationships
    groups: List[Group] = Relationship(back_populates="users")
    permissions: List[Permission] = Relationship(back_populates="users")
```

### Group and Permission Models

```python
class Group(TimestampedModel, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=150)
    description: str = Field(max_length=200)

    users: List[User] = Relationship(back_populates="groups")
    permissions: List[Permission] = Relationship(back_populates="groups")

class Permission(TimestampedModel, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codename: str = Field(unique=True, max_length=150)
    name: str = Field(max_length=150)
    description: str = Field(max_length=200)

    groups: List[Group] = Relationship(back_populates="permissions")
    users: List[User] = Relationship(back_populates="permissions")
```

## Authentication Providers

### Internal Provider

The Internal Provider handles username/password authentication with JWT tokens:

```python
from fp_admin.providers.internal import InternalProvider
from fp_admin.providers.exceptions import AuthError

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.provider = self._get_provider()

    def _get_provider(self) -> InternalProvider:
        return InternalProvider(
            secret_key=settings.SECRET_KEY,
            access_token_expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_token_expires_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
            user_auth_func=self._authenticate_user
        )

    async def _authenticate_user(self, username: str, password: str):
        # Your authentication logic here
        user = await self.get_user_by_username(username)
        if user and pwd_context.verify(password, user.password):
            return user.model_dump()
        return None

    async def authenticate_and_issue_token(self, username: str, password: str):
        return await self.provider.authenticate_and_issue_token(username, password)
```

### Provider Configuration

```python
# Custom provider configuration
provider = InternalProvider(
    secret_key="your-secret-key",
    access_token_expires_minutes=30,      # Access token lifetime
    refresh_token_expires_minutes=90,     # Refresh token lifetime
    algorithm="HS256",                    # JWT algorithm
    user_auth_func=your_auth_function     # Authentication function
)
```

## JWT Token System

### Token Structure

```python
class TokenResponse(BaseModel, Generic[T]):
    access_token: str           # Short-lived access token
    refresh_token: str          # Long-lived refresh token
    token_type: str = "bearer" # Token type
    expires_in: float          # Access token expiration timestamp
    refresh_expires_in: float  # Refresh token expiration timestamp
    user: T                   # User data
```

### Token Usage

```python
# Include token in requests
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Refresh token when access token expires
@router.post("/refresh")
async def refresh_token(request: RefreshRequest):
    user_service = UserService(session)
    return await user_service.refresh_token(
        request.refresh_token,
        request.username
    )
```

## Password Security

### Password Hashing

fp-admin uses Argon2 for secure password hashing:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Hash password
hashed_password = pwd_context.hash("user_password")

# Verify password
is_valid = pwd_context.verify("user_password", hashed_password)
```

### Password Validation

```python
from pydantic import BaseModel, validator

class SignupRequestData(BaseModel):
    username: str
    email: str
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v
```

## Role-Based Access Control

### Permission System

```python
# Define permissions
permissions = [
    Permission(codename="view_user", name="Can view user"),
    Permission(codename="add_user", name="Can add user"),
    Permission(codename="change_user", name="Can change user"),
    Permission(codename="delete_user", name="Can delete user"),
]

# Assign permissions to groups
admin_group = Group(name="Administrators")
admin_group.permissions = permissions

# Assign users to groups
user.groups.append(admin_group)
```

### Permission Checking

```python
from fp_admin.apps.auth.models import User

async def check_permission(user: User, permission_codename: str) -> bool:
    # Check user permissions
    user_permissions = [p.codename for p in user.permissions]

    # Check group permissions
    group_permissions = []
    for group in user.groups:
        group_permissions.extend([p.codename for p in group.permissions])

    all_permissions = set(user_permissions + group_permissions)
    return permission_codename in all_permissions
```

## API Authentication

### Protected Endpoints

```python
from fastapi import Depends, HTTPException
from fp_admin.providers.internal import InternalProvider

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
) -> User:
    try:
        # Decode token
        provider = InternalProvider(secret_key=settings.SECRET_KEY)
        payload = provider.decode_token(token, username)

        # Get user from database
        user = await session.get(User, payload["sub"])
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Invalid user")

        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/protected")
async def protected_endpoint(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}
```

### Permission-Based Access

```python
async def require_permission(permission_codename: str):
    async def permission_checker(current_user: User = Depends(get_current_user)):
        if not await check_permission(current_user, permission_codename):
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )
        return current_user
    return permission_checker

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_permission("delete_user"))
):
    # Only users with delete_user permission can access this
    pass
```

## Error Handling

### Authentication Errors

```python
from fp_admin.providers.exceptions import AuthError
from fp_admin.api.error_handlers import handle_validation_error

try:
    token_data = await user_service.authenticate_and_issue_token(
        username, password
    )
except AuthError:
    raise HTTPException(status_code=401, detail="Invalid credentials")
except ValidationError as e:
    raise handle_validation_error(e.details)
```

### Common Error Responses

```json
{
  "error": "Authentication failed",
  "status_code": 401,
  "details": {
    "username": ["User not found"],
    "password": ["Invalid password"]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Security Best Practices

### 1. Secret Key Management

```python
# Use environment variables
import os
SECRET_KEY = os.getenv("SECRET_KEY", "default-key-for-development")

# Generate secure keys
import secrets
SECRET_KEY = secrets.token_urlsafe(32)
```

### 2. Token Security

```python
# Short-lived access tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Secure refresh tokens
REFRESH_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60  # 7 days

# Use HTTPS in production
CORS_ORIGINS = ["https://yourdomain.com"]
```

### 3. Password Policies

```python
# Enforce strong passwords
MIN_PASSWORD_LENGTH = 8
REQUIRE_UPPERCASE = True
REQUIRE_LOWERCASE = True
REQUIRE_DIGITS = True
REQUIRE_SPECIAL_CHARS = True

# Rate limiting
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 15  # minutes
```

## Testing Authentication

### Test Configuration

```python
# tests/conftest.py
import pytest
from fp_admin import FastAPIAdmin
from fp_admin.apps.auth import *

@pytest.fixture
def app():
    return FastAPIAdmin()

@pytest.fixture
def client(app):
    return TestClient(app)

@pytest.fixture
def test_user(session):
    user = User(
        username="testuser",
        email="test@example.com",
        password="hashed_password"
    )
    session.add(user)
    session.commit()
    return user
```

### Authentication Tests

```python
# tests/test_auth.py
def test_user_signup(client):
    response = client.post("/auth/signup", json={
        "data": {
            "username": "newuser",
            "email": "new@example.com",
            "password": "SecurePass123!"
        }
    })
    assert response.status_code == 200
    assert "USER CREATED" in response.json()["message"]

def test_user_signin(client, test_user):
    response = client.post("/auth/signin", json={
        "data": {
            "username": "testuser",
            "password": "SecurePass123!"
        }
    })
    assert response.status_code == 200
    assert "access_token" in response.json()["data"]
```

## Next Steps

- **[Admin Models](../admin-models.md)** - Configure admin interface for users
- **[CLI Commands](../cli-commands.md)** - Create users from command line
- **[Field Types](../field-types.md)** - Customize user form fields
- **[API Reference](../../api/models.md)** - Authentication API endpoints
