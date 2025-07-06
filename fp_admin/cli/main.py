from getpass import getpass

import typer
import subprocess
from pathlib import Path
from importlib.metadata import version as metadata_version
from sqlmodel import select

from fp_admin.core.db import get_session

fp_cli = typer.Typer()
ALEMBIC = "alembic.ini"


def run(cmd: list[str]) -> None:
    typer.echo(f"🔧 Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


@fp_cli.command()
def version() -> None:
    typer.echo(metadata_version("fp-admin"))


@fp_cli.command()
def startproject(name: str) -> None:
    """Create a new apps with models.py, views.py, admin.py, routers.py and apps.py."""
    project_dir = Path(name)
    if project_dir.exists():
        typer.echo("❌ Project already exists.")
        raise typer.Exit(code=1)

    def render_template(template_name: str) -> None:
        (project_dir / f"{template_name}.py").write_text(
            (
                Path(__file__).parent
                / "templates"
                / "startproject"
                / f"{template_name}.tpl"
            )
            .read_text()
            .format(app_name=name, App=name.title())
        )

    project_dir.mkdir(parents=True)
    Path(project_dir / "apps").mkdir()
    for template in ["app", "settings"]:
        render_template(template)

    typer.echo(f"✅ Project '{name}' created")


@fp_cli.command()
def startapp(name: str) -> None:
    """Create a new apps with models.py, views.py, admin.py, routers.py and apps.py."""
    app_dir = Path("apps") / name
    if app_dir.exists():
        typer.echo("❌ App already exists.")
        raise typer.Exit(code=1)
    if not Path("apps").exists():
        typer.echo("❌ Apps doeos not exists.")

    def render_template(template_name: str) -> None:
        (app_dir / f"{template_name}.py").write_text(
            (Path(__file__).parent / "templates" / "startapp" / f"{template_name}.tpl")
            .read_text()
            .format(app_name=name, App=name.title())
        )

    app_dir.mkdir(parents=True)
    (app_dir / "__init__.py").touch()
    for template in ["admin", "models", "views", "routers", "apps"]:
        render_template(template)

    typer.echo(f"✅ App '{name}' created at apps/{name}/")


@fp_cli.command()
def make_migrations(
    name: str = typer.Option(..., "--name", "-n", help="Migration name")
) -> None:
    """Generate a new Alembic migration."""
    if not Path("migrations").exists():
        template_path = (
            Path(__file__).parent.parent / "core" / "alembic_template"
        ).as_posix()
        run(["alembic", "init", "migrations", "-t", template_path])
    run(["alembic", "-c", str(ALEMBIC), "revision", "--autogenerate", "-m", name])


@fp_cli.command()
def migrate() -> None:
    """Apply latest Alembic migrations."""
    run(["alembic", "-c", str(ALEMBIC), "upgrade", "head"])


@fp_cli.command()
def createsuperuser() -> None:
    """Create an models user."""
    from fp_admin.apps.auth.models import User  # Local import to ensure model is loaded

    username = typer.prompt("Username")
    email = typer.prompt("Email")
    password = getpass("Password: ")
    confirm = getpass("Confirm Password: ")
    # password = bcrypt.hash(password)

    if password != confirm:
        typer.echo("❌ Passwords do not match.")
        raise typer.Exit(code=1)

    with get_session() as session:
        stmt = select(User).where(User.username == username)
        exists = session.exec(stmt).first()
        if exists:
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
        session.commit()
        typer.echo("✅ Superuser created successfully.")
