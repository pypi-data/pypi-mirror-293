"""Text Line Detector Resource Module."""

from ..dataclasses.text_line_detect import TextLineDetectorMeta
from .base import AsyncResource, SyncResource

from typing import Dict,List

class SyncTextLineDetectorResource(SyncResource):
    """Synchronous text line detection resource"""

    def detect(
        self,
        pages_image: List[str],
        model: str = "text-line-detection"
    ) -> TextLineDetectorMeta:
        
        """Text line detection"""
        task = "text-line-detection"
        input_data = {"pages_image": pages_image}
        
        output = self._post(
            data={
                "input_data": input_data,
                "task": task,
                "model": model
            },
        )
        
        output.raise_for_status()
        return TextLineDetectorMeta(
            text_lines_detected=output.json()["output"]
            )


class AsyncTextLineDetectorResource(AsyncResource):
    """Asynchronous text line detection resource"""

    async def detect(
        self,
        pages_image: List[str],
        model: str = "text-line-detection",
        read_timeout: float = 10.0,
        timeout: float = 180.0,
    ) -> TextLineDetectorMeta:
        """Embed all texts."""
        task = "text-line-detection"
        input_data = {"pages_image": pages_image}
            
        output = await self._post(
            data={
                "input_data": input_data,
                "task": task,
                "model": model
            },
            read_timeout=read_timeout,
            timeout=timeout
        )
        
        output.raise_for_status()
        return TextLineDetectorMeta(
            text_lines_detected=output.json()["output"]
            )
