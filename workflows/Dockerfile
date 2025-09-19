# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY workflows/pyproject.toml ./pyproject.toml
RUN pip install --upgrade pip && pip install -e .

# Copy app code
COPY workflows/app ./app

# Default to worker
ENV APP_TEMPORAL_ADDRESS=temporal-frontend:7233 \
    APP_TASK_QUEUE=doc-pipeline \
    APP_LOG_LEVEL=INFO

CMD ["python", "-m", "app.worker"]
