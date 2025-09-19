from __future__ import annotations

import logging
import os
from typing import Any, Mapping

import structlog


def configure_logging(level: str | int = "INFO") -> None:
    numeric_level = logging.getLevelName(level) if isinstance(level, str) else level

    logging.basicConfig(
        format="%(message)s",
        stream=os.sys.stdout,
        level=numeric_level,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(sort_keys=True),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
