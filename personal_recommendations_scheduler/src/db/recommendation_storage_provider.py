import logging
from abc import ABC, abstractmethod

from core.config import mongo_settings
from pymongo import MongoClient

logger = logging.getLogger(__name__)


class IRecommendationStorageProvider(ABC):
    @abstractmethod
    def update(self, filters: dict, value: dict):
        pass


class MongoRecommendationStorageProvider(IRecommendationStorageProvider):
    def __init__(self, client: MongoClient, db_name: str, collection: str):
        self.client = client
        self.db = self.client[db_name]
        self.collection = collection

    def update(self, filters: dict, value: dict):
        if self.db[self.collection].find_one(filters):
            self.db[self.collection].update_one(filters, {"$set": value}, upsert=True)
        else:
            self.db[self.collection].insert_one(value)


def get_recommendation_storage_provider() -> IRecommendationStorageProvider:
    return MongoRecommendationStorageProvider(
        client=MongoClient(mongo_settings.get_url()),
        db_name=mongo_settings.mongo_db_name,
        collection=mongo_settings.collection_user_recommendation,
    )
