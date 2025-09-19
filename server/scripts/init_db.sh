#!/usr/bin/env bash
set -euo pipefail

: "${SQL_HOST:?}"
: "${SQL_PORT:=6432}"
: "${SQL_USER:?}"
: "${SQL_PASSWORD:?}"
: "${SQL_DB:?}"

export PGPASSWORD="$SQL_PASSWORD"

# Create DB if not exists (idempotent)
psql -h "$SQL_HOST" -p "$SQL_PORT" -U "$SQL_USER" -tc "SELECT 1 FROM pg_database WHERE datname = " | grep -q 1 || \
  psql -h "$SQL_HOST" -p "$SQL_PORT" -U "$SQL_USER" -c "CREATE DATABASE \"$SQL_DB\";"

# Apply Temporal schemas via admin tools container norms are handled in Render job
