# Temporal Orchestration Platform - Architecture Overview

## Project Purpose
This is a production-grade Temporal deployment demonstrating document processing workflows with key orchestration patterns including:
- **Orchestration**: Parent-child workflow relationships
- **Async Activities**: Long-running tasks with heartbeats
- **Fire-and-Forget**: Non-blocking child workflows
- **Retry Policies**: Robust error handling

## Architecture Components

### 1. Infrastructure (Render Platform)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │ Elasticsearch   │    │   PgBouncer     │
│   (Database)    │◄───┤ (Visibility)    │    │ (Connection     │
│                 │    │                 │    │  Pooling)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Temporal Server │
                    │ (4 Services)    │
                    │ - Frontend      │
                    │ - History       │
                    │ - Matching      │
                    │ - Worker        │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Temporal UI   │
                    │ (Web Interface) │
                    └─────────────────┘
```

### 2. Application Layer (Python Workflows)

#### Workflow Hierarchy
```
OrchestratorWorkflow (Parent)
├── DocumentWorkflow (Child) × N documents
│   ├── fetch_document (Activity)
│   ├── ocr_pages (Activity with heartbeats)
│   ├── classify (Activity)
│   ├── extract_entities (Activity)
│   ├── store_result (Activity with heartbeats)
│   └── AnalyticsWorkflow (Fire-and-forget child)
└── Results aggregation
```

#### Data Models
- **DocumentSpec**: Individual document with URL and priority
- **BatchRequest**: Collection of documents to process
- **Processing Results**: OCR, classification, and entity extraction results

### 3. Key Workflow Patterns

#### Document Processing Pipeline
1. **Fetch**: Download document from URL
2. **OCR**: Extract text from pages (with progress heartbeats)
3. **Classify**: Determine document type
4. **Extract**: Pull out key entities
5. **Store**: Save results (with progress heartbeats)
6. **Analytics**: Background processing (fire-and-forget)

#### Error Handling & Resilience
- **Retry Policies**: Configurable retry logic for activities
- **Timeouts**: Heartbeat and start-to-close timeouts
- **Circuit Breakers**: External service error handling
- **Graceful Degradation**: Continues processing other documents if one fails

## File Structure

```
workflows/app/
├── workflows/
│   └── orchestrator.py      # Main workflow definitions
├── activities/
│   ├── fetch.py            # Document downloading
│   └── processing.py       # OCR, classification, extraction
├── models.py               # Pydantic data models
├── config.py              # Application settings
├── worker.py              # Temporal worker process
├── cli.py                 # Command-line interface
├── logging.py             # Structured logging
└── exceptions.py          # Custom exceptions
```

## Deployment Options

### 1. Local Development
- Uses Helm charts for local Kubernetes
- DevContainer support
- Temporal UI accessible locally

### 2. Production (Render)
- Multi-service deployment
- Managed PostgreSQL and Elasticsearch
- Auto-scaling worker processes
- Public Temporal UI

## Key Features Demonstrated

1. **Parallel Processing**: Multiple documents processed concurrently
2. **Progress Tracking**: Heartbeats show real-time progress
3. **Fault Tolerance**: Retry policies and error handling
4. **Observability**: Structured logging and Temporal UI
5. **Scalability**: Horizontal scaling of workers
6. **Production Ready**: Proper configuration and monitoring

## Usage Examples

### Start Worker
```bash
python -m app.worker
```

### Submit Batch
```bash
python -m app.cli https://example.com/doc1.pdf https://example.com/doc2.pdf
```

### Monitor via UI
- Access Temporal UI to see workflow execution
- View parent-child relationships
- Monitor activity heartbeats and progress
- Debug failed workflows
