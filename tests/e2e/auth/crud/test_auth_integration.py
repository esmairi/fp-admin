import pytest
from sqlmodel import Session, select

from fp_admin.apps.auth.models import Group, Permission, User


class TestAuthModelIntegration:
    """Integration tests for auth models and their relationships."""

    def test_complete_auth_workflow(self, session: Session, auth_workflow_data):
        """Test a complete authentication workflow with users,
        groups, and permissions."""
        permissions = auth_workflow_data["permissions"]
        groups = auth_workflow_data["groups"]
        users = auth_workflow_data["users"]

        # Verify relationships
        session.refresh(users[0])  # john_doe
        session.refresh(users[1])  # jane_smith
        session.refresh(users[2])  # admin_user
        session.refresh(users[3])  # inactive_user
        session.refresh(groups[0])  # users
        session.refresh(groups[2])  # admins

        # Check user-group relationships
        assert len(users[0].groups) == 1
        assert users[0].groups[0].name == "users"
        assert len(users[1].groups) == 1
        assert users[1].groups[0].name == "editors"
        assert len(users[2].groups) == 1
        assert users[2].groups[0].name == "admins"
        assert len(users[3].groups) == 1
        assert users[3].groups[0].name == "users"

        # Check group-user relationships
        assert len(groups[0].users) == 2  # john_doe and inactive_user
        assert len(groups[2].users) == 1  # admin_user

        # Check group-permission relationships
        assert len(groups[0].permissions) == 1
        assert groups[0].permissions[0].codename == "can_read"
        assert len(groups[2].permissions) == 8  # all permissions
        admin_perms = [perm.codename for perm in groups[2].permissions]
        assert "can_read" in admin_perms
        assert "can_write" in admin_perms
        assert "can_admin" in admin_perms

        # Check permission-group relationships
        assert (
            len(permissions[0].groups) == 5
        )  # users, editors, admins, moderators, viewers
        assert len(permissions[1].groups) == 3  # editors, admins, moderators

    def test_user_permission_inheritance(
        self, session: Session, sample_permissions, sample_groups, sample_users
    ):
        """Test that users inherit permissions through their groups."""
        # Create permissions
        permissions = sample_permissions[:3]  # can_read, can_write, can_delete
        session.add_all(permissions)
        session.commit()

        # Create groups with different permission sets
        viewer_group = sample_groups[4]  # viewers
        editor_group = sample_groups[1]  # editors
        admin_group = sample_groups[2]  # admins

        viewer_group.permissions = [permissions[0]]  # can_view
        editor_group.permissions = [
            permissions[0],
            permissions[1],
        ]  # can_view, can_edit
        admin_group.permissions = permissions  # all permissions

        session.add_all([viewer_group, editor_group, admin_group])
        session.commit()

        # Create users with different group memberships
        viewer_user = sample_users[5]  # viewer_user
        editor_user = sample_users[4]  # editor_user
        admin_user = sample_users[2]  # admin_user
        multi_group_user = sample_users[0]  # john_doe

        viewer_user.groups = [viewer_group]
        editor_user.groups = [editor_group]
        admin_user.groups = [admin_group]
        multi_group_user.groups = [viewer_group, editor_group]

        session.add_all([viewer_user, editor_user, admin_user, multi_group_user])
        session.commit()

        # Refresh to get relationships
        session.refresh(viewer_user)
        session.refresh(editor_user)
        session.refresh(admin_user)
        session.refresh(multi_group_user)

        # Verify user permissions through groups
        viewer_perms = set()
        for group in viewer_user.groups:
            for perm in group.permissions:
                viewer_perms.add(perm.codename)
        assert viewer_perms == {"can_read"}

        editor_perms = set()
        for group in editor_user.groups:
            for perm in group.permissions:
                editor_perms.add(perm.codename)
        assert editor_perms == {"can_read", "can_write"}

        admin_perms = set()
        for group in admin_user.groups:
            for perm in group.permissions:
                admin_perms.add(perm.codename)
        assert admin_perms == {"can_read", "can_write", "can_delete"}

        multi_perms = set()
        for group in multi_group_user.groups:
            for perm in group.permissions:
                multi_perms.add(perm.codename)
        assert multi_perms == {"can_read", "can_write"}

    def test_cascade_delete_behavior(
        self,
        session: Session,
        read_permission,
        write_permission,
        admin_group,
        user_group,
        regular_user,
        inactive_user,
    ):
        """Test cascade delete behavior for all models."""
        # Create a complete auth setup
        perm1 = read_permission
        perm2 = write_permission
        session.add_all([perm1, perm2])
        session.commit()

        group1 = admin_group
        group2 = user_group
        group1.permissions = [perm1, perm2]
        group2.permissions = [perm1]
        session.add_all([group1, group2])
        session.commit()

        user1 = regular_user
        user2 = inactive_user
        user1.groups = [group1, group2]
        user2.groups = [group1]
        session.add_all([user1, user2])
        session.commit()

        # Store IDs for verification
        user1_id = user1.id
        user2_id = user2.id
        group1_id = group1.id
        group2_id = group2.id
        perm1_id = perm1.id
        perm2_id = perm2.id

        # Delete user1
        session.delete(user1)
        session.commit()

        # Verify user1 is deleted
        stmt = select(User).where(User.id == user1_id)
        result = session.exec(stmt).first()
        assert result is None

        # Verify user2 still exists
        stmt = select(User).where(User.id == user2_id)
        result = session.exec(stmt).first()
        assert result is not None

        # Verify groups still exist
        stmt = select(Group).where(Group.id == group1_id)
        result = session.exec(stmt).first()
        assert result is not None

        stmt = select(Group).where(Group.id == group2_id)
        result = session.exec(stmt).first()
        assert result is not None

        # Verify permissions still exist
        stmt = select(Permission).where(Permission.id == perm1_id)
        result = session.exec(stmt).first()
        assert result is not None

        stmt = select(Permission).where(Permission.id == perm2_id)
        result = session.exec(stmt).first()
        assert result is not None

        # Delete group1
        session.delete(group1)
        session.commit()

        # Verify group1 is deleted
        stmt = select(Group).where(Group.id == group1_id)
        result = session.exec(stmt).first()
        assert result is None

        # Verify user2 still exists but has no groups
        session.refresh(user2)
        assert len(user2.groups) == 0

        # Verify group2 still exists
        stmt = select(Group).where(Group.id == group2_id)
        result = session.exec(stmt).first()
        assert result is not None

    def test_complex_query_scenarios(self, session: Session, complex_auth_setup):
        """Test complex query scenarios involving multiple models."""
        permissions = complex_auth_setup["permissions"]
        groups = complex_auth_setup["groups"]
        users = complex_auth_setup["users"]

        # Assert permissions are created
        assert len(permissions) == 5
        for perm in permissions:
            assert perm.id is not None

        # Assert groups are created
        assert len(groups) == 3
        for group in groups:
            assert group.id is not None

        # Assert users are created
        assert len(users) == 4
        for user in users:
            assert user.id is not None

        # Test 1: Find all users who have a specific permission
        target_permission = permissions[1]  # perm_1
        users_with_perm = []
        for user in users:
            user_permissions = set()
            for group in user.groups:
                for perm in group.permissions:
                    user_permissions.add(perm.codename)
            if target_permission.codename in user_permissions:
                users_with_perm.append(user)

        # perm_1 is in groups 0 and 1, so users 0, 1, and 3 should have it
        assert len(users_with_perm) == 3
        user_indices = [int(user.username.split("_")[1]) for user in users_with_perm]
        assert 0 in user_indices
        assert 1 in user_indices
        assert 3 in user_indices

        # Test 2: Find all permissions that a specific user has
        target_user = users[3]  # User with all groups
        user_permissions = set()
        for group in target_user.groups:
            for perm in group.permissions:
                user_permissions.add(perm.codename)

        # User 3 has all groups, so should have all permissions
        assert len(user_permissions) == 5
        for i in range(5):
            assert f"perm_{i}" in user_permissions

        # Test 3: Find all groups that have a specific permission
        target_permission = permissions[2]  # perm_2
        groups_with_perm = []
        for group in groups:
            group_permissions = [perm.codename for perm in group.permissions]
            if target_permission.codename in group_permissions:
                groups_with_perm.append(group)

        # perm_2 is in groups 1 and 2
        assert len(groups_with_perm) == 2
        group_indices = [int(group.name.split("_")[1]) for group in groups_with_perm]
        assert 1 in group_indices
        assert 2 in group_indices

    def test_data_integrity_constraints(
        self, session: Session, regular_user, user_group, read_permission
    ):
        """Test data integrity constraints across all models."""
        # Test unique constraints
        # Create duplicate usernames
        user1 = regular_user
        session.add(user1)
        session.commit()

        user2 = User(
            username="user",  # Same username
            email="user2@example.com",
            password="password123",
        )
        session.add(user2)

        with pytest.raises(Exception):
            session.commit()
        session.rollback()

        # Test duplicate emails
        user3 = User(
            username="user3",
            email="user@example.com",  # Same email
            password="password123",
        )
        session.add(user3)

        with pytest.raises(Exception):
            session.commit()
        session.rollback()

        # Test duplicate group names
        group1 = user_group
        session.add(group1)
        session.commit()

        group2 = Group(name="users", description="Second group")
        session.add(group2)

        with pytest.raises(Exception):
            session.commit()
        session.rollback()

        # Test duplicate permission codenames
        perm1 = read_permission
        session.add(perm1)
        session.commit()

        perm2 = Permission(
            codename="can_read",  # Same codename
            name="Second Permission",
            description="Second permission",
        )
        session.add(perm2)

        with pytest.raises(Exception):
            session.commit()
        session.rollback()
