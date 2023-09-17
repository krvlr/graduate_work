import logging
from abc import ABC, abstractmethod
from typing import Any

from pymongo import MongoClient

logger = logging.getLogger(__name__)


class StorageProvider(ABC):
    @abstractmethod
    def update(self, collection: str, filters: dict, value: dict):
        pass


class StorageMongoProvider(StorageProvider):
    def __init__(self, client: MongoClient, db_name: str):
        self.client = client
        self.db = self.client[db_name]

    def update(self, collection: str, filters: dict, value: dict):
        if self.db[collection].find_one(filters):
            self.db[collection].update_one(filters, {"$set": value}, upsert=True)
        else:
            self.db[collection].insert_one(value)
