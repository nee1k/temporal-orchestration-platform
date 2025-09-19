from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models import DocumentSpec, BatchRequest


def test_document_spec_valid():
    doc = DocumentSpec(id="1", source_url="https://example.com/file.pdf")
    assert doc.id == "1"


def test_document_spec_invalid_url():
    with pytest.raises(ValidationError):
        DocumentSpec(id="1", source_url="not-a-url")


def test_batch_request():
    docs = [DocumentSpec(id="1", source_url="https://e.com/a"), DocumentSpec(id="2", source_url="https://e.com/b")]
    batch = BatchRequest(batch_id="b1", documents=docs)
    assert len(batch.documents) == 2
