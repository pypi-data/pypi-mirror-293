from abc import ABC, abstractmethod


class AbstractStreamer(ABC):
    @abstractmethod
    def stream(self, text: str):
        pass
