from __future__ import annotations

import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from .config import settings
from .logging import configure_logging, get_logger
from .activities.fetch import fetch_document, store_result
from .activities.processing import ocr_pages, classify, extract_entities
from .workflows.orchestrator import OrchestratorWorkflow, DocumentWorkflow, AnalyticsWorkflow


async def main() -> None:
    configure_logging(settings.log_level)
    logger = get_logger(__name__)

    client = await Client.connect(settings.temporal_address)

    logger.info("worker_start", task_queue=settings.task_queue)
    worker = Worker(
        client,
        task_queue=settings.task_queue,
        workflows=[OrchestratorWorkflow, DocumentWorkflow, AnalyticsWorkflow],
        activities=[fetch_document, store_result, ocr_pages, classify, extract_entities],
        max_concurrent_activities=50,
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
