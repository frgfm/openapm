from typing import AsyncGenerator

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.main import app


@pytest.fixture
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    # This would typically set up a test database
    # For now, we'll just mock the session
    return AsyncSession()


@pytest.fixture
def override_get_session(async_session: AsyncSession):
    async def get_session_override():
        yield async_session

    app.dependency_overrides[get_session] = get_session_override
    return async_session


@pytest.fixture(autouse=True)
def setup_db(override_get_session):
    pass
