# Workflows

The system implements a document-processing pipeline demonstrating key Temporal patterns.

## Patterns
- Orchestration: `OrchestratorWorkflow` starts `DocumentWorkflow` children in parallel and aggregates results.
- Async Activities: `fetch_document`, `store_result`, `ocr_pages`, `classify`, `extract_entities` use async I/O with retry/timeouts from workflow calls.
- Fire-and-Forget: `DocumentWorkflow` starts `AnalyticsWorkflow` without awaiting completion.
- Long-Running with Heartbeats: `ocr_pages` and `store_result` heartbeat progress periodically.

## Run Locally (devcontainer)
- Start worker: `python -m app.worker`
- Submit workload: `python -m app.cli https://example.com/a https://example.com/b`

## Observability
- Temporal UI shows parent-child relationships for batches and per-document workflows.
- Heartbeats visible in activity details for progress tracking.
