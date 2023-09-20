from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient

from core.config import sources_mongodb_settings, general_data_mongodb_settings

source_client: AsyncIOMotorClient = None
recommendations_client: AsyncIOMotorClient = None


def get_source_mongodb_client() -> AsyncIOMotorClient:
    return source_client


def get_recommendations_mongodb_client() -> AsyncIOMotorClient:
    return recommendations_client


class MongodbAdapter:
    def __init__(self, client: AsyncIOMotorClient, database: str):
        self.client = client
        self.db = self.client[database]

    async def find(self, collection: str, filters: dict, limit: int, offset: int) -> list[dict]:
        return [row async for row in self.db[collection].find(filters).skip(offset).limit(limit)]

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

    async def avg(self, collection: str, pipeline: list | dict) -> float | None:
        res = await self.db[collection].aggregate(pipeline).to_list(length=1)
        return res[0]["avg_score"] if res else 0


@lru_cache
def get_source_mongodb_adapter() -> MongodbAdapter:
    return MongodbAdapter(get_source_mongodb_client(), sources_mongodb_settings.mongo_db_name)


@lru_cache
def get_recommendations_mongodb_adapter() -> MongodbAdapter:
    return MongodbAdapter(
        get_recommendations_mongodb_client(),
        general_data_mongodb_settings.mongo_db_name,
    )
