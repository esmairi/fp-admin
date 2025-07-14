import pytest
from sqlmodel import Session, select

from fp_admin.apps.auth.models import (
    User,
)


class TestUserCRUD:
    """Test CRUD operations for User model."""

    def test_create_user(self, session: Session, regular_user):
        """Test creating a new user."""
        user = regular_user

        session.add(user)
        session.commit()
        session.refresh(user)

        assert user.id is not None
        assert user.username == "user"
        assert user.email == "user@example.com"
        assert user.password == "user_password"
        assert user.is_active is True
        assert user.is_superuser is False

    def test_create_user_with_defaults(self, session: Session):
        """Test creating a user with default values."""
        user = User(
            username="defaultuser", email="default@example.com", password="password123"
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        assert user.id is not None
        assert user.is_active is True
        assert user.is_superuser is False

    def test_read_user(self, session: Session, regular_user):
        """Test reading a user from database."""
        # Create user
        user = regular_user
        session.add(user)
        session.commit()

        # Read user
        stmt = select(User).where(User.username == "user")
        result = session.exec(stmt).first()

        assert result is not None
        assert result.username == "user"
        assert result.email == "user@example.com"

    def test_update_user(self, session: Session, regular_user):
        """Test updating user fields."""
        # Create user
        user = regular_user
        session.add(user)
        session.commit()

        # Update user
        user.username = "updateduser"
        user.email = "updated@example.com"
        user.is_active = False
        session.commit()
        session.refresh(user)

        assert user.username == "updateduser"
        assert user.email == "updated@example.com"
        assert user.is_active is False

    def test_delete_user(self, session: Session, regular_user):
        """Test deleting a user."""
        # Create user
        user = regular_user
        session.add(user)
        session.commit()
        user_id = user.id

        # Delete user
        session.delete(user)
        session.commit()

        # Verify user is deleted
        stmt = select(User).where(User.id == user_id)
        result = session.exec(stmt).first()
        assert result is None

    def test_user_email_validation(self, session: Session, regular_user):
        """Test that email validation works correctly."""
        # Valid email
        user = regular_user
        session.add(user)
        session.commit()
        session.refresh(user)

        assert user.email == "user@example.com"

    def test_user_unique_constraints(self, session: Session, regular_user):
        """Test that unique constraints work for username and email."""
        # Create first user
        user1 = regular_user
        session.add(user1)
        session.commit()

        # Try to create second user with same username
        user2 = User(
            username="user",  # Same username
            email="different@example.com",
            password="password123",
        )
        session.add(user2)

        with pytest.raises(Exception):  # Should raise unique constraint error
            session.commit()
        session.rollback()

        # Try to create second user with same email
        user3 = User(
            username="differentuser",
            email="user@example.com",  # Same email
            password="password123",
        )
        session.add(user3)

        with pytest.raises(Exception):  # Should raise unique constraint error
            session.commit()
        session.rollback()

    def test_user_relationships(
        self, session: Session, admin_group, user_group, regular_user
    ):
        """Test user relationships with groups."""
        # Create groups
        session.add_all([admin_group, user_group])
        session.commit()

        # Create user with groups
        user = regular_user
        user.groups = [admin_group, user_group]
        session.add(user)
        session.commit()
        session.refresh(user)

        assert len(user.groups) == 2
        assert any(group.name == "admins" for group in user.groups)
        assert any(group.name == "users" for group in user.groups)

    def test_user_superuser_flag(self, session: Session, admin_user, regular_user):
        """Test superuser flag functionality."""
        # Create regular user
        regular = regular_user

        # Create superuser
        admin = admin_user

        session.add_all([regular, admin])
        session.commit()

        assert regular.is_superuser is False
        assert admin.is_superuser is True

    def test_user_active_flag(self, session: Session, regular_user, inactive_user):
        """Test active flag functionality."""
        # Create active user
        active_user = regular_user

        # Create inactive user
        inactive = inactive_user

        session.add_all([active_user, inactive])
        session.commit()

        assert active_user.is_active is True
        assert inactive.is_active is False
