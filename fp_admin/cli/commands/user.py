"""
User management commands for fp-admin CLI.
"""

from getpass import getpass

import typer
from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fp_admin.core import get_session

user_app = typer.Typer(name="user", help="User management commands")


@user_app.command()
async def createsuperuser(session: AsyncSession = Depends(get_session)) -> None:
    """Create a superuser account.

    Examples:
        fp-admin user createsuperuser
        fp-admin createsuperuser

    This will:
        1. Prompt for username, email, and password
        2. Validate password confirmation
        3. Check for existing users
        4. Create superuser with full admin privileges

    Note:
        Password input is hidden for security
    """
    from fp_admin.apps.auth.models import User  # Local import to ensure model is loaded

    username = typer.prompt("Username")
    email = typer.prompt("Email")
    password = getpass("Password: ")
    confirm = getpass("Confirm Password: ")
    # password = bcrypt.hash(password)

    if password != confirm:
        typer.echo("❌ Passwords do not match.")
        raise typer.Exit(code=1)

    stmt = select(User).where(User.username == username)
    exists = await session.exec(stmt)
    if exists.first():
        typer.echo("❌ A user with that username already exists.")
        raise typer.Exit(code=1)

    user = User(
        username=username,
        email=email,
        password=password,  # You should hash this in production
        is_active=True,
        is_superuser=True,
    )
    session.add(user)
    await session.commit()
    typer.echo("✅ Superuser created successfully.")
