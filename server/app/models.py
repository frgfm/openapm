# Copyright (C) 2024, François-Guillaume Fernandez.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0> for full license details.

from datetime import datetime

from sqlmodel import Field, SQLModel

__all__ = ["Transaction"]


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    id: int = Field(None, primary_key=True)
    # application_id: int = Field(..., foreign_key="applications.id", nullable=False)
    timestamp: datetime
    method: str
    path: str
    status: int
    process_time: float
    client_host: str
    forwarded_for: str | None
    # Backup
    logged_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


# class Application(SQLModel, table=True):
#     __tablename__ = "applications"
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(..., nullable=False)
