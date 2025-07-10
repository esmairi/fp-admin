import pytest
from sqlmodel import Session, select

from fp_admin.apps.auth.models import (
    Group,
    GroupPermissionLink,
    Permission,
    User,
    UserGroupLink,
)


class TestUserGroupLinkCRUD:
    """Test CRUD operations for UserGroupLink model."""

    def test_create_user_group_link(self, session: Session, regular_user, user_group):
        """Test creating a user-group link."""
        # Create user and group
        user = regular_user
        group = user_group
        session.add_all([user, group])
        session.commit()

        # Create link
        link = UserGroupLink(user_id=user.id, group_id=group.id)
        session.add(link)
        session.commit()

        assert link.user_id == user.id
        assert link.group_id == group.id

    def test_create_multiple_user_group_links(
        self, session: Session, sample_users, sample_groups
    ):
        """Test creating multiple user-group links."""
        # Create users and groups
        users = sample_users[:3]
        groups = sample_groups[:3]

        session.add_all(users + groups)
        session.commit()

        # Create links
        links = []
        for i in range(3):
            link = UserGroupLink(user_id=users[i].id, group_id=groups[i].id)
            links.append(link)

        session.add_all(links)
        session.commit()

        assert len(links) == 3
        for i, link in enumerate(links):
            assert link.user_id == users[i].id
            assert link.group_id == groups[i].id

    def test_user_group_link_unique_constraint(
        self, session: Session, regular_user, user_group
    ):
        """Test that user-group link unique constraint works."""
        # Create user and group
        user = regular_user
        group = user_group
        session.add_all([user, group])
        session.commit()

        # Create first link
        link1 = UserGroupLink(user_id=user.id, group_id=group.id)
        session.add(link1)
        session.commit()

        # Try to create duplicate link
        link2 = UserGroupLink(
            user_id=user.id, group_id=group.id  # Same user  # Same group
        )
        session.add(link2)

        with pytest.raises(Exception):  # Should raise unique constraint error
            session.commit()
        session.rollback()

    def test_delete_user_group_link(self, session: Session, regular_user, user_group):
        """Test deleting a user-group link."""
        # Create user and group
        user = regular_user
        group = user_group
        session.add_all([user, group])
        session.commit()

        # Create link
        link = UserGroupLink(user_id=user.id, group_id=group.id)
        session.add(link)
        session.commit()

        # Delete link
        session.delete(link)
        session.commit()

        # Verify link is deleted
        stmt = select(UserGroupLink).where(
            UserGroupLink.user_id == user.id, UserGroupLink.group_id == group.id
        )
        result = session.exec(stmt).first()
        assert result is None

    def test_query_user_group_links(
        self, session: Session, sample_users, sample_groups
    ):
        """Test querying user-group links."""
        # Create users and groups
        user1 = sample_users[0]  # john_doe
        user2 = sample_users[1]  # jane_smith
        group1 = sample_groups[0]  # users
        group2 = sample_groups[1]  # editors
        session.add_all([user1, user2, group1, group2])
        session.commit()

        # Create links
        link1 = UserGroupLink(user_id=user1.id, group_id=group1.id)
        link2 = UserGroupLink(user_id=user1.id, group_id=group2.id)
        link3 = UserGroupLink(user_id=user2.id, group_id=group1.id)
        session.add_all([link1, link2, link3])
        session.commit()

        # Query links for user1
        stmt = select(UserGroupLink).where(UserGroupLink.user_id == user1.id)
        results = session.exec(stmt).all()
        assert len(results) == 2

        # Query links for group1
        stmt = select(UserGroupLink).where(UserGroupLink.group_id == group1.id)
        results = session.exec(stmt).all()
        assert len(results) == 2


class TestGroupPermissionLinkCRUD:
    """Test CRUD operations for GroupPermissionLink model."""

    def test_create_group_permission_link(
        self, session: Session, user_group, read_permission
    ):
        """Test creating a group-permission link."""
        # Create group and permission
        group = user_group
        permission = read_permission
        session.add_all([group, permission])
        session.commit()

        # Create link
        link = GroupPermissionLink(group_id=group.id, permission_id=permission.id)
        session.add(link)
        session.commit()

        assert link.group_id == group.id
        assert link.permission_id == permission.id

    def test_create_multiple_group_permission_links(
        self, session: Session, sample_groups, sample_permissions
    ):
        """Test creating multiple group-permission links."""
        # Create groups and permissions
        groups = sample_groups[:3]
        permissions = sample_permissions[:3]

        session.add_all(groups + permissions)
        session.commit()

        # Create links
        links = []
        for i in range(3):
            link = GroupPermissionLink(
                group_id=groups[i].id, permission_id=permissions[i].id
            )
            links.append(link)

        session.add_all(links)
        session.commit()

        assert len(links) == 3
        for i, link in enumerate(links):
            assert link.group_id == groups[i].id
            assert link.permission_id == permissions[i].id

    def test_group_permission_link_unique_constraint(
        self, session: Session, user_group, read_permission
    ):
        """Test that group-permission link unique constraint works."""
        # Create group and permission
        group = user_group
        permission = read_permission
        session.add_all([group, permission])
        session.commit()

        # Create first link
        link1 = GroupPermissionLink(group_id=group.id, permission_id=permission.id)
        session.add(link1)
        session.commit()

        # Try to create duplicate link
        link2 = GroupPermissionLink(
            group_id=group.id,  # Same group
            permission_id=permission.id,  # Same permission
        )
        session.add(link2)

        with pytest.raises(Exception):  # Should raise unique constraint error
            session.commit()
        session.rollback()

    def test_delete_group_permission_link(
        self, session: Session, user_group, read_permission
    ):
        """Test deleting a group-permission link."""
        # Create group and permission
        group = user_group
        permission = read_permission
        session.add_all([group, permission])
        session.commit()

        # Create link
        link = GroupPermissionLink(group_id=group.id, permission_id=permission.id)
        session.add(link)
        session.commit()

        # Delete link
        session.delete(link)
        session.commit()

        # Verify link is deleted
        stmt = select(GroupPermissionLink).where(
            GroupPermissionLink.group_id == group.id,
            GroupPermissionLink.permission_id == permission.id,
        )
        result = session.exec(stmt).first()
        assert result is None

    def test_query_group_permission_links(
        self, session: Session, sample_groups, sample_permissions
    ):
        """Test querying group-permission links."""
        # Create groups and permissions
        group1 = sample_groups[0]  # users
        group2 = sample_groups[1]  # editors
        perm1 = sample_permissions[0]  # can_read
        perm2 = sample_permissions[1]  # can_write
        session.add_all([group1, group2, perm1, perm2])
        session.commit()

        # Create links
        link1 = GroupPermissionLink(group_id=group1.id, permission_id=perm1.id)
        link2 = GroupPermissionLink(group_id=group1.id, permission_id=perm2.id)
        link3 = GroupPermissionLink(group_id=group2.id, permission_id=perm1.id)
        session.add_all([link1, link2, link3])
        session.commit()

        # Query links for group1
        stmt = select(GroupPermissionLink).where(
            GroupPermissionLink.group_id == group1.id
        )
        results = session.exec(stmt).all()
        assert len(results) == 2

        # Query links for perm1
        stmt = select(GroupPermissionLink).where(
            GroupPermissionLink.permission_id == perm1.id
        )
        results = session.exec(stmt).all()
        assert len(results) == 2

    def test_link_models_cascade_behavior(
        self, session: Session, regular_user, admin_group, read_permission
    ):
        """Test cascade behavior when related models are deleted."""
        # Create user, group, and permission
        user = regular_user
        group = admin_group
        permission = read_permission
        session.add_all([user, group, permission])
        session.commit()

        # Create links
        user_group_link = UserGroupLink(user_id=user.id, group_id=group.id)
        group_perm_link = GroupPermissionLink(
            group_id=group.id, permission_id=permission.id
        )
        session.add_all([user_group_link, group_perm_link])
        session.commit()

        # Store IDs for verification
        user_id = user.id
        group_id = group.id
        permission_id = permission.id

        # Delete group
        session.delete(group)
        session.commit()

        # Verify group is deleted
        stmt = select(Group).where(Group.id == group_id)
        result = session.exec(stmt).first()
        assert result is None

        # Verify links are deleted (should cascade)
        stmt = select(UserGroupLink).where(UserGroupLink.group_id == group_id)
        result = session.exec(stmt).first()
        assert result is None

        stmt = select(GroupPermissionLink).where(
            GroupPermissionLink.group_id == group_id
        )
        result = session.exec(stmt).first()
        assert result is None

        # Verify user and permission still exist
        stmt = select(User).where(User.id == user_id)
        result = session.exec(stmt).first()
        assert result is not None

        stmt = select(Permission).where(Permission.id == permission_id)
        result = session.exec(stmt).first()
        assert result is not None
