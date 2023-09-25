import json
from abc import ABC, abstractmethod
from uuid import UUID

from core.config import user_data_settings
from redis import Redis


class IUserDataProvider(ABC):
    @abstractmethod
    def search(self):
        pass


class UserDataProvider(IUserDataProvider):
    def __init__(self, redis: Redis, rating_pattern: str):
        self.redis = redis
        self.rating_pattern = rating_pattern

    def search(self):
        keys = []

        for key in self.redis.scan_iter(match=self.rating_pattern):
            keys.append(key.decode())
        return keys

    def mget(self, keys: list):
        values = self.redis.mget(keys=keys)
        return [value.decode() for value in values]


def get_user_data_provider():
    return UserDataProvider(
        redis=Redis(host=user_data_settings.host, port=user_data_settings.port),
        rating_pattern=user_data_settings.rating_pattern,
    )
