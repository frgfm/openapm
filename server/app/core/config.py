# Copyright (C) 2024, François-Guillaume Fernandez.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0> for full license details.

import os
import socket
from typing import Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["settings"]


class Settings(BaseSettings):
    # State
    PROJECT_NAME: str = "OpenAPM API"
    PROJECT_DESCRIPTION: str = "Backend operations monitoring service."
    VERSION: str = "0.1.0.dev0"
    API_V1_STR: str = "/api/v1"
    CORS_ORIGIN: str = "*"
    SUPPORT_EMAIL: str = os.environ.get("SUPPORT_EMAIL", "support@email.com")
    # DB
    POSTGRES_URL: str = os.environ["POSTGRES_URL"]

    @field_validator("POSTGRES_URL")
    @classmethod
    def sqlachmey_uri(cls, v: str) -> str:
        # Fix for SqlAlchemy 1.4+
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        return v

    # Error monitoring
    SENTRY_DSN: Union[str, None] = os.environ.get("SENTRY_DSN")
    SERVER_NAME: str = os.environ.get("SERVER_NAME", socket.gethostname())

    @field_validator("SENTRY_DSN")
    @classmethod
    def sentry_dsn_can_be_blank(cls, v: str) -> Union[str, None]:
        if not isinstance(v, str) or len(v) == 0:
            return None
        return v

    DEBUG: bool = os.environ.get("DEBUG", "").lower() != "false"
    LOGO_URL: str = ""

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
