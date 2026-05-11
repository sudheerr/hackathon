"""Tracing hooks for future observability integration."""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def trace_span(name: str, correlation_id: str | None = None) -> AsyncIterator[None]:
    """Minimal async tracing hook placeholder."""
    logger.debug("trace.start", extra={"span": name, "correlation_id": correlation_id})
    try:
        yield
    finally:
        logger.debug("trace.end", extra={"span": name, "correlation_id": correlation_id})
