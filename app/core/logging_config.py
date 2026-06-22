"""Structured logging configuration for the CareerVerse Agent."""

from __future__ import annotations

import json
import logging
import sys
from typing import Any


class JsonFormatter(logging.Formatter):
    """Custom log formatter generating JSON-structured console messages."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as a single-line JSON string."""
        log_payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)
        # Safe extraction of request metadata if added via extra attributes
        for key in ["request_id", "method", "path", "status_code", "duration_ms"]:
            if hasattr(record, key):
                log_payload[key] = getattr(record, key)
        return json.dumps(log_payload)


def configure_logging() -> None:
    """Initialize root log settings to output structured JSON streams."""
    root_logger = logging.getLogger()
    # Remove existing handlers to prevent duplicate output logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JsonFormatter(datefmt="%Y-%m-%dT%H:%M:%S%z"))
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.INFO)

    # Clean up third-party noisy libraries
    logging.getLogger("uvicorn.access").disabled = True
