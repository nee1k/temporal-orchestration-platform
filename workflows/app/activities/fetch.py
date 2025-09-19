from __future__ import annotations

import asyncio
from typing import Sequence

import aiohttp
from temporalio import activity

from ..exceptions import ExternalServiceError
from ..logging import get_logger

logger = get_logger(__name__)


@activity.defn(name="fetch_document")
async def fetch_document(url: str) -> bytes:
    activity.heartbeat("starting")
    timeout = activity.info().heartbeat_timeout or 30
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            async with session.get(url) as resp:
                if resp.status >= 400:
                    raise ExternalServiceError(f"GET {url} -> {resp.status}")
                content = await resp.read()
        activity.heartbeat("downloaded")
        return content
    except asyncio.CancelledError:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.error("fetch_failed", url=url, error=str(exc))
        raise ExternalServiceError(str(exc)) from exc


@activity.defn(name="store_result")
async def store_result(document_id: str, data: bytes) -> str:
    # Simulate storage write with heartbeat progress
    for i in range(5):
        await asyncio.sleep(0.5)
        activity.heartbeat({"progress": (i + 1) * 20})
    return f"stored:{document_id}:{len(data)}"
