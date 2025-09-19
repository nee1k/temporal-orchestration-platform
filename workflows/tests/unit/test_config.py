from __future__ import annotations

from app.config import Settings


def test_settings_defaults():
    s = Settings()
    assert s.task_queue == "doc-pipeline"
