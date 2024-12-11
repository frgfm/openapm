from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.main import app


@pytest.fixture
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    # Create a mock session with async methods
    mock_session = MagicMock(spec=AsyncSession)

    # Mock the async methods
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    mock_session.rollback = AsyncMock()
    mock_session.exec = AsyncMock()

    return mock_session


@pytest.fixture
def override_get_session(async_session: AsyncSession):
    async def get_session_override():
        yield async_session

    app.dependency_overrides[get_session] = get_session_override
    return async_session


@pytest.fixture(autouse=True)
def setup_db(override_get_session):
    pass
