from typing import Generator

import pytest
from fastapi.testclient import TestClient

from fp_admin import FastAPIAdmin


# Register custom markers to avoid warnings
def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")


@pytest.fixture(scope="module")
def app() -> FastAPIAdmin:
    return FastAPIAdmin()


@pytest.fixture(scope="module")
def client(app: FastAPIAdmin) -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
