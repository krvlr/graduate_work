import json
import logging
from abc import ABC, abstractmethod
from typing import Optional

import aiohttp
from fastapi import status

from core.config import general_recommendations_settings, base_settings

logger = logging.getLogger(__name__)


class IGeneralRecommendationsProvider(ABC):
    @abstractmethod
    async def get(self, genres: Optional[list[str]] = None):
        pass

    @abstractmethod
    async def get_ratings(self, movies_ids: list[str]):
        pass


class GeneralRecommendationsProvider(IGeneralRecommendationsProvider):
    async def get(self, genres: Optional[list[str]] = None):
        genres_params = "&genres=" + "&genres=".join(genres) if genres else ""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                general_recommendations_settings.get_replacement_url()
                + f"?limit={base_settings.user_recommendation_size}{genres_params}"
            ) as response:
                if response.status == status.HTTP_200_OK:
                    text = await response.text()
                    return json.loads(text)

    async def get_ratings(self, movies_ids: list[str]):
        movies_ids = "movies_ids=" + "&movies_ids=".join(movies_ids)  # type: str
        async with aiohttp.ClientSession() as session:
            async with session.get(
                general_recommendations_settings.get_rating_url() + f"?{movies_ids}"
            ) as response:
                if response.status == status.HTTP_200_OK:
                    text = await response.text()
                    return json.loads(text)


def get_general_recommendations_provider():
    return GeneralRecommendationsProvider()
