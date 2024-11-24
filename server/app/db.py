# Copyright (C) 2024, François-Guillaume Fernandez.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0> for full license details.

import asyncio
import logging
import sys

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, text
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

__all__ = ["get_session", "init_db"]


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(levelname)s:     %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

engine = create_async_engine(settings.POSTGRES_URL, echo=False)


async def get_next_id(session: AsyncSession, table_name: str) -> int:
    result = await session.exec(text(f"SELECT nextval('{table_name}_id_seq')"))  # type: ignore[call-overload]
    return result.scalar()


async def get_session() -> AsyncSession:  # type: ignore[misc]
    async with AsyncSession(engine) as session:
        yield session


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # async with AsyncSession(engine) as session:
    #     logger.info("Checking PostgreSQL database state...")
    #     # Check if the table needs initialization
    #     statement = select(User).limit(1)  # type: ignore[var-annotated]
    #     results = await session.exec(statement=statement)
    #     user = results.first()
    #     if not user:
    #         logger.info("Initializing PostgreSQL database...")
    #         # Double check the organization table
    #         statement = select(Organization).limit(1)
    #         results = await session.exec(statement=statement)
    #         org = results.first()
    #         if not org:
    #             logger.info("Creating superadmin organization...")
    #             session.add(Organization(name="admins"))
    #         elif org.name != "admins":
    #             logger.error("Incorrect initialization of organization table")
    #             raise RuntimeError("DB was initialized with wrong organization name")
    #         logger.info("Creating superadmin user...")
    #         session.add(
    #             User(
    #                 email=settings.SUPERADMIN_EMAIL,
    #                 hashed_password=hash_password(settings.SUPERADMIN_PWD),
    #                 role=UserRole.SUPERADMIN,
    #                 is_confirmed=False,
    #                 organization_id=1,
    #             )
    #         )
    #     elif user.email != settings.SUPERADMIN_EMAIL:
    #         logger.error("Incorrect initialization of user table")
    #         raise RuntimeError("DB was initialized with wrong superadmin email")
    #     else:
    #         logger.info("Recovering existing PostgreSQL database...")
    #     await session.commit()


async def main() -> None:
    await init_db()


if __name__ == "__main__":
    asyncio.run(main())
