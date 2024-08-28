"""Dataclasses for classifiers."""

from typing import List

from pydantic import BaseModel


class Classification(BaseModel):
    """A classification output."""

    label: str
    confidence: float


class ClassifierMeta(BaseModel):
    """Metadata for an classifier output."""

    text: str
    classifications: List[Classification]
