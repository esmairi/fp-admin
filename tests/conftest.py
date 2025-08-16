import asyncio

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from fp_admin import FastAPIAdmin
from fp_admin.apps.auth import *  # noqa: F403, F401
from fp_admin.core import DatabaseManager
from tests.fixtures.auth.models import *  # noqa: F403, F401
from tests.fixtures.blog_models import *  # noqa: F403, F401
from tests.fixtures.models import *  # noqa: F403, F401


# Register custom markers to avoid warnings
def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def db_manager(tmp_path):
    return DatabaseManager("sqlite+aiosqlite:///{}".format(tmp_path / "test.db"))


@pytest.fixture
def engine(db_manager):
    return db_manager.engine


@pytest_asyncio.fixture
async def session(db_manager):
    async with db_manager.get_session() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def setup_db(monkeypatch, db_manager):
    """Set up database."""
    monkeypatch.setattr(DatabaseManager, "engine", db_manager.engine)
    await db_manager.init_db()


@pytest.fixture
def app(db_manager) -> FastAPIAdmin:
    return FastAPIAdmin()


@pytest.fixture
def client(app):
    return TestClient(app)
