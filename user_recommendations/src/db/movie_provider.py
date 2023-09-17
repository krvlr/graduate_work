import json
import logging
from abc import ABC, abstractmethod
from uuid import UUID

import aiohttp
from core.config import movie_settings
from fastapi import status

logger = logging.getLogger(__name__)


class IMovieProvider(ABC):
    @abstractmethod
    async def get(self, movie_id: UUID):
        pass


class MovieProvider(IMovieProvider):
    def __init__(self, movie_url: str):
        self.movie_url = movie_url

    async def get(self, movie_id: UUID):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.movie_url + f"/{str(movie_id)}") as response:
                if response.status == status.HTTP_200_OK:
                    text = await response.text()
                    return json.loads(text)


def get_movie_provider():
    return MovieProvider(movie_url=movie_settings.get_url())
