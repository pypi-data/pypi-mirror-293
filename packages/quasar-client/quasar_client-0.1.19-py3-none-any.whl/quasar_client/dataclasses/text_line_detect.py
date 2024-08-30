"""Dataclasses for text line detection."""
from typing import Any, Dict, List
from pydantic import BaseModel


class TextLineDetectorMeta(BaseModel):
    """Metadata for text line detection output."""

    text_lines_detected: List[Dict[str, Any]]
