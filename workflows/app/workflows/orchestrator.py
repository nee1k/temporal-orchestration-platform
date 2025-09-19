from __future__ import annotations

from typing import Iterable

from temporalio import workflow
from temporalio.common import RetryPolicy

from ..models import DocumentSpec, BatchRequest

# Child workflow stubs (defined below)


@workflow.defn
class DocumentWorkflow:
    @workflow.run
    async def run(self, spec: DocumentSpec) -> str:
        from ..activities.fetch import fetch_document, store_result
        from ..activities.processing import ocr_pages, classify, extract_entities

        # Fetch
        content: bytes = await workflow.execute_activity(
            fetch_document,
            spec.source_url.unicode_string(),
            start_to_close_timeout=30,
            heartbeat_timeout=10,
            retry_policy=RetryPolicy(initial_interval=1, maximum_interval=10, maximum_attempts=5),
        )

        # OCR (long-running with heartbeats)
        pages: list[str] = await workflow.execute_activity(
            ocr_pages,
            spec.id,
            content,
            start_to_close_timeout=120,
            heartbeat_timeout=10,
            retry_policy=RetryPolicy(initial_interval=1, maximum_interval=30, maximum_attempts=0),
        )

        # Sequential classify + extract
        label, confidence = await workflow.execute_activity(
            classify,
            spec.id,
            pages,
            start_to_close_timeout=30,
            retry_policy=RetryPolicy(initial_interval=1, maximum_interval=10, maximum_attempts=3),
        )
        entities = await workflow.execute_activity(
            extract_entities,
            spec.id,
            pages,
            start_to_close_timeout=30,
            retry_policy=RetryPolicy(initial_interval=1, maximum_interval=10, maximum_attempts=3),
        )

        # Store result
        result = await workflow.execute_activity(
            store_result,
            spec.id,
            f"{label}:{confidence}:{entities}".encode(),
            start_to_close_timeout=60,
            heartbeat_timeout=10,
        )

        # Fire-and-forget analytics workflow
        workflow.start_child_workflow(AnalyticsWorkflow.run, spec.id)

        return result


@workflow.defn
class AnalyticsWorkflow:
    @workflow.run
    async def run(self, document_id: str) -> None:  # fire-and-forget: no return awaited by parent
        # Simulate async analytics work via timer
        await workflow.sleep(5)


@workflow.defn
class OrchestratorWorkflow:
    @workflow.run
    async def run(self, batch: BatchRequest) -> list[str]:
        # Start child workflows in parallel for concurrency
        child_futures = [
            workflow.start_child_workflow(
                DocumentWorkflow.run,
                spec,
                id=f"docwf-{spec.id}",
                task_queue=workflow.info().task_queue,
                retry_policy=RetryPolicy(initial_interval=2, maximum_interval=10, maximum_attempts=0),
            )
            for spec in batch.documents
        ]
        results = [await f for f in child_futures]
        return results
