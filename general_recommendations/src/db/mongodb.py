from functools import lru_cache

import pymongo
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import general_data_mongodb_settings

recommendations_client: AsyncIOMotorClient = None


def get_recommendations_mongodb_client() -> AsyncIOMotorClient:
    return recommendations_client


class MongodbAdapter:
    def __init__(self, client: AsyncIOMotorClient, database: str):
        self.client = client
        self.db = self.client[database]

    async def find(
        self,
        collection: str,
        filters: dict,
        limit: int,
        offset: int,
        sort: str | list[str] | None = None,
        direction: None | int = None,
    ) -> list[dict]:
        if sort:
            return [
                row
                async for row in self.db[collection]
                .find(filters)
                .skip(offset)
                .limit(limit)
                .sort(sort, direction)
            ]
        else:
            return [
                row async for row in self.db[collection].find(filters).skip(offset).limit(limit)
            ]

    async def find_one(self, collection: str, filters: dict) -> dict | None:
        return await self.db[collection].find_one(filters)

    async def insert(self, collection: str, data: dict) -> None:
        await self.db[collection].insert_one(data)

    async def update(self, collection: str, filters: dict, data: dict) -> None:
        await self.db[collection].update_one(filters, {"$set": data}, upsert=True)

    async def delete(self, collection: str, filters: dict) -> None:
        await self.db[collection].find_one_and_delete(filters)

    async def delete_all(self, collection: str) -> None:
        await self.db[collection].delete_many({})

    async def count(self, collection: str, filters: dict) -> int | None:
        return await self.db[collection].count_documents(filters)


@lru_cache
def get_mongodb_adapter(
    data_provider=Depends(get_recommendations_mongodb_client),
) -> MongodbAdapter:
    return MongodbAdapter(data_provider, general_data_mongodb_settings.mongo_db_name)
