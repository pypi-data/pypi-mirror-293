"""Dataclasses for VIT layout element classification."""
from typing import Any, Dict, List
from pydantic import BaseModel


class VITLayoutElementClassifierMeta(BaseModel):
    """Metadata for vit based layout element classification output."""

    layout_elements_classified: List[Dict[str, Any]]
