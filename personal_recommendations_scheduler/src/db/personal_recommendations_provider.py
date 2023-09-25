import json
import logging
from abc import ABC, abstractmethod
from http import HTTPStatus
from uuid import UUID

import aiohttp
from core.config import personal_recommendations_settings

logger = logging.getLogger(__name__)


class IPersonalRecommendationsProvider(ABC):
    @abstractmethod
    async def personal(self, data: dict):
        pass


class PersonalRecommendationsProvider(IPersonalRecommendationsProvider):
    def __init__(self, personal_recommendations_url: str):
        self.personal_recommendations_url = personal_recommendations_url

    async def personal(self, data: dict):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.personal_recommendations_url, json=data) as response:
                if response.status == HTTPStatus.OK:
                    text = await response.text()
                    return json.loads(text)


def get_personal_recommendations_provider():
    return PersonalRecommendationsProvider(
        personal_recommendations_url=personal_recommendations_settings.get_url()
    )
