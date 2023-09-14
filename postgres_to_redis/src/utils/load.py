import json
import logging

from uuid import UUID
from abc import ABC, abstractmethod
from utils.utils import backoff
from datetime import timedelta
from typing import Any, Union, Generator
from db.storage_provider import StorageProvider, StorageRedisProvider

from redis import Redis

logger = logging.getLogger(__name__)


class Loader(ABC):
    @abstractmethod
    def save_data(self, batch_transformer: Generator):
        pass


class RedisLoader(Loader):
    def __init__(self, storage: StorageProvider):
        self.storage = storage

    @backoff()
    def save_data(self, batch_transformer: Generator):
        for key, value in batch_transformer:
            self.storage.update(key=key, value=json.dumps(value))
