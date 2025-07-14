import pytest

from fp_admin.apps.auth.models import (
    Group,
    Permission,
    User,
)


@pytest.fixture
def sample_permissions():
    """Sample permissions for testing."""
    return [
        Permission(
            codename="can_read",
            name="Can Read",
            description="Permission to read resources",
        ),
        Permission(
            codename="can_write",
            name="Can Write",
            description="Permission to write resources",
        ),
        Permission(
            codename="can_delete",
            name="Can Delete",
            description="Permission to delete resources",
        ),
        Permission(
            codename="can_admin",
            name="Can Admin",
            description="Administrative permissions",
        ),
        Permission(
            codename="can_view",
            name="Can View",
            description="Permission to view resources",
        ),
        Permission(
            codename="can_edit",
            name="Can Edit",
            description="Permission to edit resources",
        ),
        Permission(
            codename="user_management",
            name="User Management",
            description="Permission to manage users",
        ),
        Permission(
            codename="system_config",
            name="System Configuration",
            description="Permission to configure system settings",
        ),
    ]


@pytest.fixture
def sample_groups():
    """Sample groups for testing."""
    return [
        Group(name="users", description="Regular users"),
        Group(name="editors", description="Content editors"),
        Group(name="admins", description="System administrators"),
        Group(name="moderators", description="Content moderators"),
        Group(name="viewers", description="Read-only users"),
    ]


@pytest.fixture
def sample_users():
    """Sample users for testing."""
    return [
        User(
            username="john_doe",
            email="john.doe@example.com",
            password="hashed_password_123",
            is_active=True,
            is_superuser=False,
        ),
        User(
            username="jane_smith",
            email="jane.smith@example.com",
            password="hashed_password_456",
            is_active=True,
            is_superuser=False,
        ),
        User(
            username="admin_user",
            email="admin@example.com",
            password="admin_password_789",
            is_active=True,
            is_superuser=True,
        ),
        User(
            username="inactive_user",
            email="inactive@example.com",
            password="password_123",
            is_active=False,
            is_superuser=False,
        ),
        User(
            username="editor_user",
            email="editor@example.com",
            password="editor_password_123",
            is_active=True,
            is_superuser=False,
        ),
        User(
            username="viewer_user",
            email="viewer@example.com",
            password="viewer_password_123",
            is_active=True,
            is_superuser=False,
        ),
    ]


@pytest.fixture
def admin_user():
    """Admin user fixture."""
    return User(
        username="admin",
        email="admin@example.com",
        password="admin_password",
        is_active=True,
        is_superuser=True,
    )


@pytest.fixture
def regular_user():
    """Regular user fixture."""
    return User(
        username="user",
        email="user@example.com",
        password="user_password",
        is_active=True,
        is_superuser=False,
    )


@pytest.fixture
def inactive_user():
    """Inactive user fixture."""
    return User(
        username="inactive",
        email="inactive@example.com",
        password="password",
        is_active=False,
        is_superuser=False,
    )


@pytest.fixture
def admin_group():
    """Admin group fixture."""
    return Group(name="admins", description="System administrators")


@pytest.fixture
def user_group():
    """User group fixture."""
    return Group(name="users", description="Regular users")


@pytest.fixture
def editor_group():
    """Editor group fixture."""
    return Group(name="editors", description="Content editors")


@pytest.fixture
def viewer_group():
    """Viewer group fixture."""
    return Group(name="viewers", description="Read-only users")


@pytest.fixture
def read_permission():
    """Read permission fixture."""
    return Permission(
        codename="can_read", name="Can Read", description="Permission to read resources"
    )


@pytest.fixture
def write_permission():
    """Write permission fixture."""
    return Permission(
        codename="can_write",
        name="Can Write",
        description="Permission to write resources",
    )


@pytest.fixture
def delete_permission():
    """Delete permission fixture."""
    return Permission(
        codename="can_delete",
        name="Can Delete",
        description="Permission to delete resources",
    )


@pytest.fixture
def admin_permission():
    """Admin permission fixture."""
    return Permission(
        codename="can_admin", name="Can Admin", description="Administrative permissions"
    )


@pytest.fixture
def view_permission():
    """View permission fixture."""
    return Permission(
        codename="can_view", name="Can View", description="Permission to view resources"
    )


@pytest.fixture
def edit_permission():
    """Edit permission fixture."""
    return Permission(
        codename="can_edit", name="Can Edit", description="Permission to edit resources"
    )


@pytest.fixture
def user_management_permission():
    """User management permission fixture."""
    return Permission(
        codename="user_management",
        name="User Management",
        description="Permission to manage users",
    )


@pytest.fixture
def system_config_permission():
    """System configuration permission fixture."""
    return Permission(
        codename="system_config",
        name="System Configuration",
        description="Permission to configure system settings",
    )


@pytest.fixture
def auth_workflow_data(session, sample_permissions, sample_groups, sample_users):
    """Complete auth workflow data with relationships."""
    # Add all permissions
    session.add_all(sample_permissions)
    session.commit()

    # Add all groups
    session.add_all(sample_groups)
    session.commit()

    # Assign permissions to groups
    sample_groups[0].permissions = [sample_permissions[0]]  # users -> can_read
    sample_groups[1].permissions = [
        sample_permissions[0],
        sample_permissions[1],
    ]  # editors -> can_read, can_write
    sample_groups[2].permissions = sample_permissions  # admins -> all permissions
    sample_groups[3].permissions = [
        sample_permissions[0],
        sample_permissions[1],
        sample_permissions[2],
    ]  # moderators -> read, write, delete
    sample_groups[4].permissions = [sample_permissions[0]]  # viewers -> can_read
    session.commit()

    # Add all users
    session.add_all(sample_users)
    session.commit()

    # Assign users to groups
    sample_users[0].groups = [sample_groups[0]]  # john_doe -> users
    sample_users[1].groups = [sample_groups[1]]  # jane_smith -> editors
    sample_users[2].groups = [sample_groups[2]]  # admin_user -> admins
    sample_users[3].groups = [sample_groups[0]]  # inactive_user -> users
    sample_users[4].groups = [sample_groups[1]]  # editor_user -> editors
    sample_users[5].groups = [sample_groups[4]]  # viewer_user -> viewers
    session.commit()

    return {
        "permissions": sample_permissions,
        "groups": sample_groups,
        "users": sample_users,
    }


@pytest.fixture
def complex_auth_setup(session):
    """Complex auth setup with multiple relationships."""
    # Create permissions
    permissions = []
    for i in range(5):
        perm = Permission(
            codename=f"perm_{i}",
            name=f"Permission {i}",
            description=f"Permission {i} description",
        )
        permissions.append(perm)
    session.add_all(permissions)
    session.commit()

    # Create groups
    groups = []
    for i in range(3):
        group = Group(name=f"group_{i}", description=f"Group {i} description")
        groups.append(group)
    session.add_all(groups)
    session.commit()

    # Assign permissions to groups
    groups[0].permissions = permissions[:2]  # First 2 permissions
    groups[1].permissions = permissions[1:4]  # Middle 3 permissions
    groups[2].permissions = permissions[2:]  # Last 3 permissions
    session.commit()

    # Create users
    users = []
    for i in range(4):
        user = User(
            username=f"user_{i}", email=f"user{i}@example.com", password="password123"
        )
        users.append(user)
    session.add_all(users)
    session.commit()

    # Assign users to groups
    users[0].groups = [groups[0]]  # Only first group
    users[1].groups = [groups[1]]  # Only second group
    users[2].groups = [groups[2]]  # Only third group
    users[3].groups = groups  # All groups
    session.commit()

    return {"permissions": permissions, "groups": groups, "users": users}
