# Copyright (C) 2024, François-Guillaume Fernandez.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0> for full license details.

import logging
import time
from datetime import datetime

import sentry_sdk
from fastapi import Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.crud import TransactionCRUD
from app.db import get_session
from app.models import Transaction

logger = logging.getLogger("uvicorn.error")

# Sentry
if isinstance(settings.SENTRY_DSN, str):
    sentry_sdk.init(
        settings.SENTRY_DSN,
        enable_tracing=False,
        traces_sample_rate=0.0,
        profiles_sample_rate=0.0,
        integrations=[
            StarletteIntegration(transaction_style="url"),
            FastApiIntegration(transaction_style="url"),
        ],
        release=settings.VERSION,
        server_name=settings.SERVER_NAME,
        debug=settings.DEBUG,
        environment=None if settings.DEBUG else "production",
    )
    logger.info(f"Sentry middleware enabled on server {settings.SERVER_NAME}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    debug=settings.DEBUG,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=None,
)


class Status(BaseModel):
    status: str


# Healthcheck
@app.get(
    "/status",
    status_code=status.HTTP_200_OK,
    summary="Healthcheck for the API",
    include_in_schema=False,
)
def get_status() -> Status:
    return Status(status="ok")


def get_transaction_crud(session: AsyncSession = Depends(get_session)) -> TransactionCRUD:
    return TransactionCRUD(session=session)


class TransactionPayload(BaseModel):
    method: str
    path: str
    status: int
    process_time: float
    client_host: str
    forwarded_for: str | None
    timestamp: datetime


# Routes
@app.post(
    "/transaction", status_code=status.HTTP_201_CREATED, summary="Log a backend operation", include_in_schema=True
)
async def log_transaction(
    payload: TransactionPayload, transactions: TransactionCRUD = Depends(get_transaction_crud)
) -> Transaction:
    return await transactions.create(payload)


# Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if isinstance(settings.SENTRY_DSN, str):
    app.add_middleware(SentryAsgiMiddleware)


# Overrides swagger to include favicon
@app.get("/docs", include_in_schema=False)
def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        title=settings.PROJECT_NAME,
        swagger_favicon_url="https://cdn.worldvectorlogo.com/logos/openai-2.svg",
        # Remove schemas from swagger
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )


# OpenAPI config
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    # https://fastapi.tiangolo.com/tutorial/metadata/
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.PROJECT_DESCRIPTION,
        routes=app.routes,
        license_info={
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
        },
        contact={
            "name": "API support",
            "email": settings.SUPPORT_EMAIL,
            "url": "https://github.com/frgfm/openapm/issues",
        },
    )
    openapi_schema["info"]["x-logo"] = {"url": "https://cdn.worldvectorlogo.com/logos/openai-2.svg"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore[method-assign]
