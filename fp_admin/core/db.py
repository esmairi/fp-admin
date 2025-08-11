import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from fp_admin.exceptions import DatabaseError
from fp_admin.settings_loader import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database manager for handling connections and sessions."""

    _engine: AsyncEngine

    def __init__(self, database_url: str, echo: bool = False):
        """Initialize database manager.

        Args:
            database_url: Database connection URL
            echo: Enable SQL query logging
        """
        self.database_url = database_url
        self.echo = echo
        self._engine = self.get_session_engine()

    @property
    def engine(self) -> AsyncEngine:
        """Database engine instance."""
        return self._engine

    def get_session_engine(self) -> AsyncEngine:
        """Get database engine, creating it if necessary."""
        try:
            logger.info("Creating database engine for %s", self.database_url)
            return create_async_engine(self.database_url, echo=self.echo)
        except Exception as e:
            logger.error("Failed to create database engine: %s", e)
            raise DatabaseError(f"Failed to create database engine: {e}") from e

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database async session with automatic cleanup.

        Yields:
            Database Async session

        Example:
            with db_manager.get_session() as session:
                result = session.exec(select(User)).all()
        """
        async with AsyncSession(self.engine) as session:
            yield session

    async def init_db(self) -> None:
        """Create all database tables."""
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error("Failed to create database tables: %s", e)
            raise DatabaseError(f"Failed to create database tables: {e}") from e


# # Global database manager instance
db_manager = DatabaseManager(
    database_url=settings.DATABASE_URL, echo=settings.DATABASE_ECHO
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database session.

    Yields:
        Database session
    """
    async with db_manager.get_session() as session:
        yield session
