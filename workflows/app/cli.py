from __future__ import annotations

import asyncio
import json
import uuid
from typing import Sequence

from temporalio.client import Client

from .config import settings
from .logging import configure_logging, get_logger
from .models import DocumentSpec, BatchRequest
from .workflows.orchestrator import OrchestratorWorkflow


async def submit_batch(urls: Sequence[str]) -> list[str]:
    configure_logging(settings.log_level)
    logger = get_logger(__name__)

    client = await Client.connect(settings.temporal_address)

    docs = [DocumentSpec(id=str(uuid.uuid4()), source_url=url) for url in urls]
    batch = BatchRequest(batch_id=str(uuid.uuid4()), documents=docs)

    handle = await client.start_workflow(
        OrchestratorWorkflow.run,
        batch,
        id=f"batch-{batch.batch_id}",
        task_queue=settings.task_queue,
    )
    logger.info("batch_started", workflow_id=handle.id, run_id=handle.first_execution_run_id)

    # Optionally wait for result (or comment for fire-and-forget from CLI)
    result = await handle.result()
    logger.info("batch_completed", result=result)
    return result


if __name__ == "__main__":
    import sys

    urls = sys.argv[1:] or [
        "https://example.com/a.pdf",
        "https://example.com/b.pdf",
        "https://example.com/c.pdf",
    ]
    asyncio.run(submit_batch(urls))
