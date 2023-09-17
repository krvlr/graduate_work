import logging
from abc import ABC, abstractmethod
from typing import Generator

from db.storage_provider import StorageProvider
from utils.utils import backoff

logger = logging.getLogger(__name__)


class Loader(ABC):
    @abstractmethod
    def save_data(self, batch_transformer: Generator):
        pass


class MongoLoader(Loader):
    def __init__(self, storage: StorageProvider):
        self.storage = storage

    @backoff()
    def save_data(self, batch_transformer: Generator):
        for collection, filters, value in batch_transformer:
            self.storage.update(collection=collection, filters=filters, value=value)
