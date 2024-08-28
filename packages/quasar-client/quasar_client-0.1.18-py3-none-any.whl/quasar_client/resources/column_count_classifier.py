"""Classifier Resource Module."""

from typing import List, Tuple

from ..dataclasses.column_count_classifier import ColumnCountClassifierMeta
from .base import AsyncResource, SyncResource


class SyncPageColumnCounterResource(SyncResource):
    """
    Synchronous Page Column Counter Resource Class.
    pages_images_base64_string: List of base64 encoded images of page, 
    bboxes: List of bounding boxes of words in the page (order: x0, y0, x1, y1),
    words: List of words in the page
    """

    def classify(
        self,
        pages_images_base64_string: List[str],
        bboxes: List[List[Tuple[int, int, int, int]]], 
        words: List[List[str]],
    ) -> ColumnCountClassifierMeta:
        """Column classification of every page"""
        
        task = "column-count-classification"
        input_data = {
                "pages_images_base64_string": pages_images_base64_string, 
                "bboxes": bboxes, 
                "words": words}
        
        output = self._post(
            data={
                "input_data": input_data,
                "task": task,
            },
        )
        
        output.raise_for_status()
        return ColumnCountClassifierMeta(
            column_counts=output.json()["output"]
        )


class AsyncPageColumnCounterResource(AsyncResource):
    """
    Asynchronous Page Column Counter Resource Class.
    pages_images_base64_string: List of base64 encoded images of page, 
    bboxes: List of bounding boxes of words in the page (order: x0, y0, x1, y1),
    words: List of words in the page
    """

    async def classify(
        self,
        pages_images_base64_string: List[str],
        bboxes: List[List[Tuple[int, int, int, int]]], 
        words: List[List[str]],
        read_timeout: float = 10.0,
        timeout: float = 180.0,
    ) -> ColumnCountClassifierMeta:
        """Column classification of every page"""
        
        task = "column-count-classification"
        input_data = {
            "pages_images_base64_string": pages_images_base64_string, 
            "bboxes": bboxes, 
            "words": words
        }
            
        output = await self._post(
            data={
                "input_data": input_data,
                "task": task,
            },
            read_timeout=read_timeout,
            timeout=timeout
        )
        
        output.raise_for_status()
        return ColumnCountClassifierMeta(
            column_counts=output.json()["output"]
        )
