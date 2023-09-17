import logging
from abc import ABC, abstractmethod

from core.config import mongo_settings
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


client: AsyncIOMotorClient = None


def get_mongodb_client() -> AsyncIOMotorClient:
    return client


class IRecommendationStorageProvider(ABC):
    @abstractmethod
    async def get(self, collection: str, filters: dict) -> dict | None:
        pass


class StorageMongoProvider(IRecommendationStorageProvider):
    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        self.client = client
        self.db = self.client[db_name]

    async def get(self, collection: str, filters: dict) -> dict | None:
        res = await self.db[collection].find_one(filters)
        return res


def get_recommendation_provider(
    client=Depends(get_mongodb_client),
):
    return StorageMongoProvider(client=client, db_name=mongo_settings.mongo_db_name)
