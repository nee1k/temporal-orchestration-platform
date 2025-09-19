# Deployment on Render.com

This runbook describes deploying a production-style Temporal cluster on Render using the blueprint in `render/render.yaml`.

## Components
- PostgreSQL 15 (private service) with PgBouncer connection pooling
- Elasticsearch 7.17 (single node) with persistent disk
- Temporal services: frontend, history, matching, worker
- Temporal UI (public web service)
- Admin Tools job for schema setup and default namespace registration

## Sequence
1. Create environment variable groups in Render to match `envVarGroups` in the blueprint (`postgres-auth`, `temporal-core`, `ui-config`).
2. Deploy `postgres` (private) with 10GB disk.
3. Deploy `pgbouncer` (private) pointing to `postgres`.
4. Deploy `elasticsearch` (private) with 20GB disk.
5. Run `admin-tools` job to initialize DB schemas and register `default` namespace (idempotent).
6. Deploy Temporal services in order: `temporal-frontend`, then `temporal-history`, `temporal-matching`, `temporal-worker`.
7. Deploy `temporal-ui` (public). It discovers the frontend address via the private host.

## Verification
- Temporal UI loads and shows `default` namespace.
- `tctl n list` and `tctl wf list --ns default` from the Admin Tools job.
- Trigger a workflow via `python -m app.cli` and observe executions in the UI.
- Elasticsearch contains visibility indices (`/_cat/indices`).

## Troubleshooting
- UI cannot connect: verify `TEMPORAL_ADDRESS` points to the frontend host and port 7233.
- DB connection errors: confirm PgBouncer is reachable and pool sizes are adequate.
- ES unhealthy: ensure disk is attached and `discovery.type=single-node` is set.

## Assumptions / Trade-offs
- Single ES node for simplicity. In production, run multi-node with snapshots.
- TLS is not enabled; rely on Render private networking and secret storage.
