import logging

import abc
from abc import ABCMeta
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class Event(BaseModel):
    user_id: str
    movie_id: str
    timestamp_of_film: str

    def transform(self):
        return self.user_id, self.movie_id, self.timestamp_of_film


class Transformer(metaclass=ABCMeta):
    @abc.abstractmethod
    def transform(self, event):
        pass

    @abc.abstractmethod
    def get_batch_transformer(self, events):
        pass


class DataTransformer(Transformer):
    def transform(self, event):
        return Event(
            user_id=str(event["user_id"]),
            movie_id=str(event["movie_id"]),
            timestamp_of_film=str(event["timestamp_of_film"]),
        ).transform()

    def get_batch_transformer(self, events):
        for event in events:
            transform_event = self.transform(event)
            yield transform_event