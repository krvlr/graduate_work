from abc import ABC, abstractmethod
from typing import Any

from redis import Redis


class StorageProvider(ABC):
    @abstractmethod
    def update(self, key: str, value: Any):
        pass


class StorageRedisProvider(StorageProvider):
    def __init__(self, redis: Redis):
        self.redis = redis

    def update(self, key: str, value: Any):
        self.redis.set(name=key, value=value)
