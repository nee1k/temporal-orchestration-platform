#!/usr/bin/env bash
set -euo pipefail

# Install Python tooling
PYTHON=python3.11
if ! command -v $PYTHON >/dev/null 2>&1; then
  apt-get update && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa -y && apt-get update && apt-get install -y python3.11 python3.11-venv python3.11-distutils
fi

$PYTHON -m venv /workspaces/.venv
source /workspaces/.venv/bin/activate
pip install --upgrade pip
pip install -e workflows[dev]

# Create kind cluster
if ! command -v kind >/dev/null 2>&1; then
  curl -Lo /usr/local/bin/kind https://kind.sigs.k8s.io/dl/v0.22.0/kind-linux-amd64 && chmod +x /usr/local/bin/kind
fi
kind create cluster --name temporal-dev || true

# Add helm repos
helm repo add temporal https://charts.temporal.io
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install Temporal + dependencies
helm upgrade --install postgres bitnami/postgresql --namespace temporal --create-namespace --set auth.username=temporal,auth.password=temporal,auth.database=temporal
helm upgrade --install elasticsearch bitnami/elasticsearch --namespace temporal --set master.replicas=1,data.replicas=0,coordinating.replicas=0,ingest.replicas=0 --set volumePermissions.enabled=true
helm upgrade --install temporal temporal/temporal --namespace temporal --set server.config.persistence.default.sql.user=temporal --set server.config.persistence.default.sql.password=temporal --set server.config.persistence.default.sql.host=postgresql.temporal.svc.cluster.local --set server.config.persistence.default.sql.port=5432 --set server.config.persistence.default.sql.database=temporal --set server.config.persistence.visibility.sql.user=temporal --set server.config.persistence.visibility.sql.password=temporal --set server.config.persistence.visibility.sql.host=postgresql.temporal.svc.cluster.local --set server.config.persistence.visibility.sql.port=5432 --set server.config.persistence.visibility.sql.database=temporal --set elasticsearch.enabled=true
helm upgrade --install temporal-ui temporal/temporal-ui --namespace temporal

# Port-forward UI for local access
kubectl -n temporal rollout status deploy/temporal-frontend --timeout=180s || true
