from __future__ import annotations
from abc import abstractmethod

from promptadmin.types import Message, ModelResponse, ModelServiceInfo


class BaseModelService:
    @abstractmethod
    async def execute(self, prompt: str, history: list[Message]) -> ModelResponse:
        """"""

    @abstractmethod
    def info(self) -> ModelServiceInfo:
        """"""
