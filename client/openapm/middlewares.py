# Copyright (C) 2024, François-Guillaume Fernandez.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0> for full license details.

import time
from datetime import datetime, timezone
from typing import Awaitable, Callable
from urllib.parse import urljoin

import requests
from fastapi import BackgroundTasks, FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

__all__ = ["FastAPIMiddleware"]


class FastAPIMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        endpoint: str,
    ) -> None:
        super().__init__(app)
        # Verify the endpoint
        if requests.get(urljoin(endpoint, "status"), timeout=2).status_code != 200:
            raise ValueError(f"Unable to reach endpoint: {endpoint}")
        self.endpoint = endpoint

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        ts = datetime.now(tz=timezone.utc)
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        # Log the transaction
        background_tasks = BackgroundTasks()
        background_tasks.add_task(
            requests.post,
            urljoin(self.endpoint, "transactions"),
            json={
                "timestamp": ts.isoformat(),
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "process_time": process_time,
                "client_host": request.client.host,
                "forwarded_for": request.headers.get("x-forwarded-for"),
            },
        )
        response.background = background_tasks
        return response
