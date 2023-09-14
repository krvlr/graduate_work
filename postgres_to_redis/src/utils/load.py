import json
import logging
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Generator, Union
from uuid import UUID

from db.storage_provider import StorageProvider, StorageRedisProvider
from redis import Redis
from utils.utils import backoff

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
