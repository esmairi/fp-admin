import pytest
from sqlmodel import Session, select

from fp_admin.apps.auth.models import (
    Group,
    Permission,
    User,
)


class TestGroupCRUD:
    """Test CRUD operations for Group model."""

    def test_create_group(self, session: Session, user_group):
        """Test creating a new group."""
        group = user_group

        session.add(group)
        session.commit()
        session.refresh(group)

        assert group.id is not None
        assert group.name == "users"
        assert group.description == "Regular users"

    def test_read_group(self, session: Session, user_group):
        """Test reading a group from database."""
        # Create group
        group = user_group
        session.add(group)
        session.commit()

        # Read group
        stmt = select(Group).where(Group.name == "users")
        result = session.exec(stmt).first()

        assert result is not None
        assert result.name == "users"
        assert result.description == "Regular users"

    def test_update_group(self, session: Session, user_group):
        """Test updating group fields."""
        # Create group
        group = user_group
        session.add(group)
        session.commit()

        # Update group
        group.name = "updatedgroup"
        group.description = "Updated description"
        session.commit()
        session.refresh(group)

        assert group.name == "updatedgroup"
        assert group.description == "Updated description"

    def test_delete_group(self, session: Session, user_group):
        """Test deleting a group."""
        # Create group
        group = user_group
        session.add(group)
        session.commit()
        group_id = group.id

        # Delete group
        session.delete(group)
        session.commit()

        # Verify group is deleted
        stmt = select(Group).where(Group.id == group_id)
        result = session.exec(stmt).first()
        assert result is None

    def test_group_unique_name_constraint(self, session: Session, user_group):
        """Test that group name unique constraint works."""
        # Create first group
        group1 = user_group
        session.add(group1)
        session.commit()

        # Try to create second group with same name
        group2 = Group(name="users", description="Second group")  # Same name
        session.add(group2)

        with pytest.raises(Exception):  # Should raise unique constraint error
            session.commit()
        session.rollback()

    def test_group_relationships_with_users(
        self, session: Session, user_group, regular_user, inactive_user
    ):
        """Test group relationships with users."""
        # Create users
        user1 = regular_user
        user2 = inactive_user
        session.add_all([user1, user2])
        session.commit()

        # Create group with users
        group = user_group
        group.users = [user1, user2]
        session.add(group)
        session.commit()
        session.refresh(group)

        assert len(group.users) == 2
        assert any(user.username == "user" for user in group.users)
        assert any(user.username == "inactive" for user in group.users)

    def test_group_relationships_with_permissions(
        self, session: Session, user_group, read_permission, write_permission
    ):
        """Test group relationships with permissions."""
        # Create permissions
        perm1 = read_permission
        perm2 = write_permission
        session.add_all([perm1, perm2])
        session.commit()

        # Create group with permissions
        group = user_group
        group.permissions = [perm1, perm2]
        session.add(group)
        session.commit()
        session.refresh(group)

        assert len(group.permissions) == 2
        assert any(perm.codename == "can_read" for perm in group.permissions)
        assert any(perm.codename == "can_write" for perm in group.permissions)

    def test_group_complex_relationships(
        self,
        session: Session,
        admin_group,
        user_group,
        regular_user,
        inactive_user,
        read_permission,
        write_permission,
    ):
        """Test group with both users and permissions."""
        # Create users
        user1 = regular_user
        user2 = inactive_user

        # Create permissions
        perm1 = read_permission
        perm2 = write_permission

        session.add_all([user1, user2, perm1, perm2])
        session.commit()

        # Create group with both users and permissions
        group = admin_group
        group.users = [user1, user2]
        group.permissions = [perm1, perm2]
        session.add(group)
        session.commit()
        session.refresh(group)

        assert len(group.users) == 2
        assert len(group.permissions) == 2
        assert any(user.username == "user" for user in group.users)
        assert any(user.username == "inactive" for user in group.users)
        assert any(perm.codename == "can_read" for perm in group.permissions)
        assert any(perm.codename == "can_write" for perm in group.permissions)

    def test_group_field_validation(self, session: Session, user_group):
        """Test group field validation."""
        # Test with valid data
        group = user_group
        session.add(group)
        session.commit()
        session.refresh(group)

        assert group.name == "users"
        assert group.description == "Regular users"

    def test_group_cascade_operations(
        self,
        session: Session,
        admin_group,
        user_group,
        regular_user,
        inactive_user,
        read_permission,
        write_permission,
    ):
        """Test cascade operations when group is deleted."""
        # Create users and permissions
        user1 = regular_user
        user2 = inactive_user

        perm1 = read_permission
        perm2 = write_permission

        session.add_all([user1, user2, perm1, perm2])
        session.commit()

        # Create group with relationships
        group = admin_group
        group.users = [user1, user2]
        group.permissions = [perm1, perm2]
        session.add(group)
        session.commit()

        # Store IDs for verification
        user_ids = [user1.id, user2.id]
        perm_ids = [perm1.id, perm2.id]
        group_id = group.id

        # Delete group
        session.delete(group)
        session.commit()

        # Verify group is deleted
        stmt = select(Group).where(Group.id == group_id)
        result = session.exec(stmt).first()
        assert result is None

        # Verify users still exist (should not cascade)
        for user_id in user_ids:
            stmt = select(User).where(User.id == user_id)
            result = session.exec(stmt).first()
            assert result is not None

        # Verify permissions still exist (should not cascade)
        for perm_id in perm_ids:
            stmt = select(Permission).where(Permission.id == perm_id)
            result = session.exec(stmt).first()
            assert result is not None
