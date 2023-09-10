import abc
from abc import ABCMeta

from pydantic import BaseModel


class QueueProvider(metaclass=ABCMeta):
    @abc.abstractmethod
    async def send(self, topic: str, event: dict, key: str):
        pass
