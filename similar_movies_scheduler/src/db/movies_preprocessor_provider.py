import json
import logging
from abc import ABC, abstractmethod
from http import HTTPStatus
from uuid import UUID

import aiohttp
from core.config import movies_preprocessor_settings

logger = logging.getLogger(__name__)


class IMoviesPreprocessorProvider(ABC):
    @abstractmethod
    async def vectorize(self, data: dict):
        pass


class MoviesPreprocessorProvider(IMoviesPreprocessorProvider):
    def __init__(self, movies_preprocessor_url: str):
        self.movies_preprocessor_url = movies_preprocessor_url

    async def vectorize(self, data: dict):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.movies_preprocessor_url, json=data) as response:
                if response.status == HTTPStatus.OK:
                    text = await response.text()
                    return json.loads(text)


def get_movies_preprocessing_provider():
    return MoviesPreprocessorProvider(
        movies_preprocessor_url=movies_preprocessor_settings.get_url()
    )
