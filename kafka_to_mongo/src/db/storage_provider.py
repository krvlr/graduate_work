import logging
from abc import ABC, abstractmethod
from typing import Any

from pymongo import MongoClient

logger = logging.getLogger(__name__)


class StorageProvider(ABC):
    @abstractmethod
    def update(self, collection: str, value: Any):
        pass


class StorageMongoProvider(StorageProvider):
    def __init__(self, client: MongoClient, db_name: str):
        self.client = client
        self.db = self.client[db_name]

    def update(self, collection: str, value: Any):
        if not self.db[collection].find_one(value):
            self.db[collection].insert_one(value)
