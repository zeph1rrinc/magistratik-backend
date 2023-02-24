import asyncio
from typing import Any
from typing import Generator

import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from backend.app import app
from backend.database import get_session
from backend.database.tables import Base
from backend.settings import settings

engine = create_engine("psycopg2".join(settings.database_url.split("asyncpg")))


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


async def _get_test_session():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(
            settings.database_url,
            future=True,
            echo=True,
            execution_options={"isolation_level": "AUTOCOMMIT"},
        )

        # create session for the interaction with database
        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        session = test_async_session()
        yield session
    finally:
        await session.close()


@pytest_asyncio.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_session] = _get_test_session
    with TestClient(app) as test_client:
        yield test_client
