"""Классы для хранения состояний"""

from abc import ABC, abstractmethod
import json
import os
from typing import Any


class BaseStorage(ABC):
    @abstractmethod
    def save_state(self, state: dict) -> None:
        pass

    @abstractmethod
    def retrieve_state(self) -> dict:
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, storage_path: str = "state.json"):
        self.storage_path = storage_path

    def save_state(self, state: dict) -> None:
        with open(self.storage_path, "w") as f:
            json.dump(state, f, separators=(",\n", ": "))

    def retrieve_state(self) -> dict:
        if not os.path.isfile(self.storage_path):
            return {}

        with open(self.storage_path, "r") as f:
            return json.load(f)


class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        _storage = self.storage.retrieve_state()
        _storage[key] = value
        self.storage.save_state(_storage)

    def get_state(self, key: str, default: Any) -> Any:
        return self.storage.retrieve_state().get(key, default)
