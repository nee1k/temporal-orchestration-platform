from __future__ import annotations

import asyncio
from temporalio import activity

from ..logging import get_logger

logger = get_logger(__name__)


@activity.defn(name="ocr_pages")
async def ocr_pages(document_id: str, content: bytes) -> list[str]:
    pages: list[str] = []
    total = 6
    for i in range(total):
        await asyncio.sleep(0.4)
        page_text = f"page-{i}-text"
        pages.append(page_text)
        activity.heartbeat({"doc": document_id, "page": i + 1, "total": total})
    return pages


@activity.defn(name="classify")
async def classify(document_id: str, pages: list[str]) -> tuple[str, float]:
    await asyncio.sleep(0.2)
    label = "invoice" if any("total" in p for p in pages) else "generic"
    return label, 0.92


@activity.defn(name="extract_entities")
async def extract_entities(document_id: str, pages: list[str]) -> dict[str, list[str]]:
    await asyncio.sleep(0.3)
    return {"amount": ["123.45"], "vendor": ["Acme Corp"]}
