import json
import logging
from abc import ABC, abstractmethod
from http import HTTPStatus
from uuid import UUID

import aiohttp
from core.config import similar_movies_settings

logger = logging.getLogger(__name__)


class ISimilarMoviesProvider(ABC):
    @abstractmethod
    async def nearest_neighbours(self, data: dict):
        pass


class SimilarMoviesProvider(ISimilarMoviesProvider):
    def __init__(self, similar_movies_url: str):
        self.similar_movies_url = similar_movies_url

    async def nearest_neighbours(self, data: dict):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.similar_movies_url, json=data) as response:
                if response.status == HTTPStatus.OK:
                    text = await response.text()
                    return json.loads(text)


def get_similar_movies_provider():
    return SimilarMoviesProvider(similar_movies_url=similar_movies_settings.get_url())
