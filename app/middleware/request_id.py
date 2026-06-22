"""Middleware to attach a unique request ID to each API transaction."""

from __future__ import annotations

import logging
import re
import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.middleware.request_id")

# Safe Request ID regex pattern to validate X-Request-ID format
REQUEST_ID_PATTERN = re.compile(r"^[a-zA-Z0-9\-_]{8,100}$")


class RequestIDMiddleware(BaseHTTPMiddleware):
    """FastAPI BaseHTTPMiddleware to track transaction IDs and request metrics."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Process incoming request, generate request ID, and log metrics."""
        request_id = request.headers.get("X-Request-ID") or ""
        if not REQUEST_ID_PATTERN.match(request_id):
            request_id = str(uuid.uuid4())

        # Set request state variable for application access
        request.state.request_id = request_id

        start_time = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as exc:
            # Calculate duration on failure
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(
                "Request failed: %s %s",
                request.method,
                request.url.path,
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": 500,
                    "duration_ms": duration_ms,
                },
                exc_info=True,
            )
            raise exc

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        response.headers["X-Request-ID"] = request_id

        # Logging only path and method safely to maintain data privacy rules
        logger.info(
            "HTTP %s %s -> %s (%s ms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )

        return response
