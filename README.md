# Temporal Orchestration Platform

Production-grade Temporal deployment on Render with Python workflows demonstrating orchestration, async activities, fire-and-forget, and long-running heartbeating. Includes Helm-based dev environment and optional ArgoCD GitOps.

## Contents
- Render blueprint: `render/render.yaml`
- Temporal config: `server/config/*.yaml`
- Workflows code: `workflows/app/*`
- Dev (Helm + devcontainer): `.devcontainer/*`, `deploy/helm/*`
- Docs: `docs/*`

## Quick Start (Local Dev)
1. Open in Dev Container (or install kind + helm manually).
2. In one terminal:
   ```bash
   python -m app.worker
   ```
3. In another terminal:
   ```bash
   python -m app.cli https://example.com/a https://example.com/b
   ```
4. Open Temporal UI deployed via Helm.

## Deploy to Render
- Create Blueprint from this repo, pick `render/render.yaml`.
- Verify `admin-tools` initialized schemas, then ensure all Temporal services are healthy.
- Open Temporal UI (public web service) and confirm `default` namespace.
