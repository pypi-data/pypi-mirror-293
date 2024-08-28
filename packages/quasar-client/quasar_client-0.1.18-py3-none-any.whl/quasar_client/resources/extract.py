"""Extract Resource Module."""

from typing import Literal, Optional, Union

from ..dataclasses.extract import ExtractMeta, Keyword
from .base import AsyncResource, SyncResource


class SyncExtractorResource(SyncResource):
    """Synchronous ExtractorResource Class."""

    def extract(
        self,
        text: str,
        task: Optional[Union[Literal["topics"], Literal["keyword-extraction"]]] = None,
        model: Optional[str] = None,
        priority: int = 0,
        **kwargs,
    ) -> ExtractMeta:
        """Extract keywords or topics."""
        data = {
            "input_data": {"docs": [text], **kwargs},
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
        extract_response = output.json()["output"]
        return ExtractMeta(
            text=text,
            keywords=[
                Keyword(
                    keyword=kw["keyword"],
                    score=kw["score"],
                )
                for kw in extract_response[0]["keywords"]
            ],
        )


class AsyncExtractorResource(AsyncResource):
    """Asynchronous Extractor Resource Class."""

    async def extract(
        self,
        text: str,
        task: Optional[Union[Literal["topics"], Literal["keyword-extraction"]]] = None,
        model: Optional[str] = None,
        read_timeout: float = 10.0,
        timeout: float = 180.0,
        priority: int = 0,
        **kwargs,
    ) -> ExtractMeta:
        """Extract keywords or topics."""
        data = {
            "input_data": {"docs": [text], **kwargs},
            "task": task,
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
        extract_response = output.json()["output"]
        return ExtractMeta(
            text=text,
            keywords=[
                Keyword(
                    keyword=kw["keyword"],
                    score=kw["score"],
                )
                for kw in extract_response[0]["keywords"]
            ],
        )
