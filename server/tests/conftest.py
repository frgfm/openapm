import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, text
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import engine
from app.main import app


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://api.localhost:5050", follow_redirects=True) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session_maker() as session:
        async with session.begin():
            for table in reversed(SQLModel.metadata.sorted_tables):
                await session.exec(table.delete())
                if hasattr(table.c, "id"):
                    await session.exec(text(f"ALTER SEQUENCE {table.name}_id_seq RESTART WITH 1"))

        yield session
        await session.rollback()
