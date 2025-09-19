# Dev Environment

A devcontainer provisions a local Kubernetes (kind) cluster and installs Temporal via Helm.

## Steps
1. Open repository in VS Code with Dev Containers extension.
2. Devcontainer builds and runs `post-create.sh` to:
   - Install Python 3.11 and dependencies
   - Create a kind cluster `temporal-dev`
   - Install Postgres, Elasticsearch, Temporal server, and UI via Helm
3. Port-forward or use `kubectl proxy` to access services; UI is exposed via the `temporal-ui` service.

## Worker & CLI
- Worker: `python -m app.worker`
- Submit batch: `python -m app.cli https://example.com/a`

## Notes
- Values: `deploy/helm/temporal/values.yaml` controls Temporal chart configuration.
- To tear down: `kind delete cluster --name temporal-dev`.
