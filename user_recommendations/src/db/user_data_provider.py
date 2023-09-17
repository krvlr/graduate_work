import json
from abc import ABC, abstractmethod
from uuid import UUID

from core.config import redis_settings
from fastapi import Depends
from redis.asyncio import Redis

redis: Redis | None = None


def get_redis():
    return redis


class IStorageUserDataProvider(ABC):
    @abstractmethod
    async def get(self, user_id: UUID):
        pass


class StorageRedisProvider(IStorageUserDataProvider):
    def __init__(self, redis: Redis, key: str):
        self.redis = redis
        self.key = key

    def get_key(self, user_id: UUID):
        return f"{str(user_id)}:{self.key}"

    async def get(self, user_id: UUID):
        key = self.get_key(user_id=user_id)
        user_profile = await self.redis.get(name=key)

        if user_profile:
            return json.loads(user_profile.decode())


def get_user_data_provider(redis=Depends(get_redis)):
    return StorageRedisProvider(redis=redis, key=redis_settings.user_profile_key)
