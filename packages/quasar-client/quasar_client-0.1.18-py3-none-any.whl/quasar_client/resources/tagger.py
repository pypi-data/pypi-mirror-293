"""Tagger Resource Module."""

from typing import List, Literal, Optional, Union

from ..dataclasses.tag import TaggerMeta
from .base import AsyncResource, SyncResource


class SyncTaggerResource(SyncResource):
    """Synchronous Tagger Resource Class."""

    def tag(
        self,
        text: str,
        task: Optional[Union[Literal["ner"], Literal["acronym-detection"]]] = None,
        model: Optional[str] = None,
        priority: int = 0,
    ) -> List[TaggerMeta]:
        """Tag a text."""
        data = {
            "input_data": {"docs": [text]},
            "priority": priority,
        }
        if model:
            data["model"] = model
        elif task:
            data["task"] = task
        else:
            raise ValueError("Either `task` or `model` must be provided.")
        output = self._post(data=data)
        output.raise_for_status()
        return [
            TaggerMeta(
                end=entity["char_end_index"],
                label=entity["label"],
                score=entity["score"],
                span=entity["span"],
                start=entity["char_start_index"],
            )
            for entity in output.json()["output"][0]
        ]


class AsyncTaggerResource(AsyncResource):
    """Asynchronous Tagger Resource Class."""

    async def tag(
        self,
        text: str,
        task: Optional[Union[Literal["ner"], Literal["acronym-detection"]]] = None,
        model: Optional[str] = None,
        priority: int = 0,
        read_timeout: float = 10.0,
        timeout: float = 180.0,
    ) -> List[TaggerMeta]:
        """Tag a text."""
        data = {
            "input_data": {"docs": [text]},
            "priority": priority,
        }
        if model:
            data["model"] = model
        elif task:
            data["task"] = task
        else:
            raise ValueError("Either `task` or `model` must be provided.")
        output = await self._post(
            data=data,
            read_timeout=read_timeout,
            timeout=timeout,
        )
        output.raise_for_status()
        return [
            TaggerMeta(
                end=entity["char_end_index"],
                label=entity["label"],
                score=entity["score"],
                span=entity["span"],
                start=entity["char_start_index"],
            )
            for entity in output.json()["output"][0]
        ]
