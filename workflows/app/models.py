from __future__ import annotations

from pydantic import BaseModel, HttpUrl, Field, PositiveInt, conlist


class DocumentSpec(BaseModel):
    id: str = Field(min_length=1)
    source_url: HttpUrl
    priority: int = Field(ge=0, le=10, default=5)


class BatchRequest(BaseModel):
    batch_id: str
    documents: conlist(DocumentSpec, min_length=1)  # type: ignore[type-arg]


class OCRResult(BaseModel):
    document_id: str
    pages: list[str]


class ClassificationResult(BaseModel):
    document_id: str
    label: str
    confidence: float


class ExtractionResult(BaseModel):
    document_id: str
    entities: dict[str, list[str]]

