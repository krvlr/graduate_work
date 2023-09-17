import logging
from abc import ABC, abstractmethod
from typing import Generator

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Transformer(ABC):
    @abstractmethod
    def transform(self, topic: str, event: dict):
        pass

    @abstractmethod
    def get_batch_transformer(self, batch_extractor: Generator):
        pass


class DataTransformer(Transformer):
    def __init__(self, topic_to_model: dict):
        self.topic_to_model = topic_to_model

    def transform(self, topic: str, event: dict):
        return self.topic_to_model[topic](**event).transform()

    def get_batch_transformer(self, batch_extractor: Generator):
        for topic, event in batch_extractor:
            collection, filters, transform_event = self.transform(topic=topic, event=event)
            yield collection, filters, transform_event
