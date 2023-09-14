import logging

from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Generator

from models.movie import UserProfile

logger = logging.getLogger(__name__)


class Transformer(ABC):
    @abstractmethod
    def transform(self, event: dict):
        pass

    @abstractmethod
    def get_batch_transformer(self, batch_extractor: Generator):
        pass


class DataTransformer(Transformer):
    def transform(self, event: dict):
        return UserProfile(**event).transform()

    def get_batch_transformer(self, batch_extractor: Generator):
        for batch in batch_extractor:
            for event in batch:
                transform_event = self.transform(event=event)
                yield transform_event
