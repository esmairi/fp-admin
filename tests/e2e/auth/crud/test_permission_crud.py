import pytest
from sqlmodel import Session, select

from fp_admin.apps.auth.models import (
    Group,
    Permission,
)


class TestPermissionCRUD:
    """Test CRUD operations for Permission model."""

    def test_create_permission(self, session: Session, read_permission):
        """Test creating a new permission."""
        permission = read_permission

        session.add(permission)
        session.commit()
        session.refresh(permission)

        assert permission.id is not None
        assert permission.codename == "can_read"
        assert permission.name == "Can Read"
        assert permission.description == "Permission to read resources"

    def test_read_permission(self, session: Session, read_permission):
        """Test reading a permission from database."""
        # Create permission
        permission = read_permission
        session.add(permission)
        session.commit()

        # Read permission
        stmt = select(Permission).where(Permission.codename == "can_read")
        result = session.exec(stmt).first()

        assert result is not None
        assert result.codename == "can_read"
        assert result.name == "Can Read"
        assert result.description == "Permission to read resources"

    def test_update_permission(self, session: Session, read_permission):
        """Test updating permission fields."""
        # Create permission
        permission = read_permission
        session.add(permission)
        session.commit()

        # Update permission
        permission.name = "Updated Permission"
        permission.description = "Updated description"
        session.commit()
        session.refresh(permission)

        assert permission.name == "Updated Permission"
        assert permission.description == "Updated description"

    def test_delete_permission(self, session: Session, read_permission):
        """Test deleting a permission."""
        # Create permission
        permission = read_permission
        session.add(permission)
        session.commit()
        permission_id = permission.id

        # Delete permission
        session.delete(permission)
        session.commit()

        # Verify permission is deleted
        stmt = select(Permission).where(Permission.id == permission_id)
        result = session.exec(stmt).first()
        assert result is None

    def test_permission_unique_codename_constraint(
        self, session: Session, read_permission
    ):
        """Test that permission codename unique constraint works."""
        # Create first permission
        perm1 = read_permission
        session.add(perm1)
        session.commit()

        # Try to create second permission with same codename
        perm2 = Permission(
            codename="can_read",  # Same codename
            name="Different Permission",
            description="Second permission",
        )
        session.add(perm2)

        with pytest.raises(Exception):  # Should raise unique constraint error
            session.commit()
        session.rollback()

    def test_permission_relationships_with_groups(
        self, session: Session, admin_group, user_group, read_permission
    ):
        """Test permission relationships with groups."""
        # Create groups
        group1 = admin_group
        group2 = user_group
        session.add_all([group1, group2])
        session.commit()

        # Create permission with groups
        permission = read_permission
        permission.groups = [group1, group2]
        session.add(permission)
        session.commit()
        session.refresh(permission)

        assert len(permission.groups) == 2
        assert any(group.name == "admins" for group in permission.groups)
        assert any(group.name == "users" for group in permission.groups)

    def test_permission_field_validation(self, session: Session, read_permission):
        """Test permission field validation."""
        # Test with valid data
        permission = read_permission
        session.add(permission)
        session.commit()
        session.refresh(permission)

        assert permission.codename == "can_read"
        assert permission.name == "Can Read"
        assert permission.description == "Permission to read resources"

    def test_permission_cascade_operations(
        self, session: Session, admin_group, user_group, read_permission
    ):
        """Test cascade operations when permission is deleted."""
        # Create groups
        group1 = admin_group
        group2 = user_group
        session.add_all([group1, group2])
        session.commit()

        # Create permission with relationships
        permission = read_permission
        permission.groups = [group1, group2]
        session.add(permission)
        session.commit()

        # Store IDs for verification
        group_ids = [group1.id, group2.id]
        permission_id = permission.id

        # Delete permission
        session.delete(permission)
        session.commit()

        # Verify permission is deleted
        stmt = select(Permission).where(Permission.id == permission_id)
        result = session.exec(stmt).first()
        assert result is None

        # Verify groups still exist (should not cascade)
        for group_id in group_ids:
            stmt = select(Group).where(Group.id == group_id)
            result = session.exec(stmt).first()
            assert result is not None

    def test_permission_codename_format(self, session: Session):
        """Test permission codename format validation."""
        # Test various codename formats
        valid_codenames = [
            "can_read",
            "can_write",
            "can_delete",
            "can_admin",
            "user_management",
            "system_config",
        ]

        for i, codename in enumerate(valid_codenames):
            permission = Permission(
                codename=codename,
                name=f"Permission {i}",
                description=f"Description for {codename}",
            )
            session.add(permission)

        session.commit()

        # Verify all permissions were created
        stmt = select(Permission)
        results = session.exec(stmt).all()
        assert len(results) == len(valid_codenames)

    def test_permission_name_length(self, session: Session):
        """Test permission name length constraints."""
        # Test with maximum length name
        long_name = "A" * 150  # Maximum length
        permission = Permission(
            codename="long_name_test", name=long_name, description="Test with long name"
        )
        session.add(permission)
        session.commit()
        session.refresh(permission)

        assert permission.name == long_name

    def test_permission_description_length(self, session: Session):
        """Test permission description length constraints."""
        # Test with maximum length description
        long_description = "A" * 200  # Maximum length
        permission = Permission(
            codename="long_desc_test",
            name="Long Description Test",
            description=long_description,
        )
        session.add(permission)
        session.commit()
        session.refresh(permission)

        assert permission.description == long_description

    def test_permission_complex_relationships(
        self,
        session: Session,
        sample_groups,
        read_permission,
        write_permission,
        delete_permission,
    ):
        """Test permission with complex group relationships."""
        # Create multiple groups
        groups = sample_groups[:3]  # Use first 3 groups

        # Create permissions
        permissions = [read_permission, write_permission, delete_permission]

        session.add_all(groups + permissions)
        session.commit()

        # Create permission with all groups
        permission = Permission(
            codename="complex_permission",
            name="Complex Permission",
            description="Permission with many groups",
        )
        permission.groups = groups
        session.add(permission)
        session.commit()
        session.refresh(permission)

        assert len(permission.groups) == 3
        for group in groups:
            assert any(g.name == group.name for g in permission.groups)

    def test_permission_query_by_codename(
        self, session: Session, read_permission, write_permission, delete_permission
    ):
        """Test querying permissions by codename."""
        # Create multiple permissions
        permissions = [read_permission, write_permission, delete_permission]

        session.add_all(permissions)
        session.commit()

        # Query by codename
        stmt = select(Permission).where(Permission.codename == "can_write")
        result = session.exec(stmt).first()

        assert result is not None
        assert result.codename == "can_write"
        assert result.name == "Can Write"

    def test_permission_query_by_name(self, session: Session, read_permission):
        """Test querying permissions by name."""
        # Create permission
        permission = read_permission
        session.add(permission)
        session.commit()

        # Query by name
        stmt = select(Permission).where(Permission.name == "Can Read")
        result = session.exec(stmt).first()

        assert result is not None
        assert result.codename == "can_read"
        assert result.name == "Can Read"
