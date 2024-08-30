"""Ranker Resource Module."""

from typing import List, Optional, Tuple

from ..dataclasses.rank import RankerMeta
from .base import AsyncResource, SyncResource


class SyncRankerResource(SyncResource):
    """Synchronous Ranker Resource Class."""

    def rank(
        self,
        pairs: List[Tuple[str, str]],
        priority: int = 0,
        model: Optional[str] = None,
    ) -> List[RankerMeta]:
        """Rank pairs of text."""
        data = {
            "input_data": {"pairs": pairs},
            "priority": priority,
        }
        if model:
            data["model"] = model
        else:
            data["task"] = "ranking"
        output = self._post(data=data)
        output.raise_for_status()
        return [
            RankerMeta(
                pair=(pair["query"], pair["candidate"]),
                score=pair["score"],
            )
            for pair in output.json()["output"]
        ]


class AsyncRankerResource(AsyncResource):
    """Asynchronous Ranker Resource Class."""

    async def rank(
        self,
        pairs: List[Tuple[str, str]],
        model: Optional[str] = None,
        read_timeout: float = 10.0,
        timeout: float = 180.0,
        priority: int = 0,
    ) -> List[RankerMeta]:
        """Asynchronously rank pairs of text."""
        data = {
            "input_data": {"pairs": pairs},
            "priority": priority,
        }
        if model:
            data["model"] = model
        else:
            data["task"] = "ranking"
        response = await self._post(
            data=data,
            read_timeout=read_timeout,
            timeout=timeout,
        )
        response.raise_for_status()
        return [
            RankerMeta(
                pair=(pair["query"], pair["candidate"]),
                score=pair["score"],
            )
            for pair in response.json()["output"]
        ]
