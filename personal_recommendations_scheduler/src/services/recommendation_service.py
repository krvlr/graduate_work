import logging

from core.config import personal_recommendations_settings
from db.personal_recommendations_provider import (
    IPersonalRecommendationsProvider,
    get_personal_recommendations_provider,
)
from db.recommendation_storage_provider import (
    IRecommendationStorageProvider,
    get_recommendation_storage_provider,
)
from db.user_data_provider import IUserDataProvider, get_user_data_provider
from models.user import PersonalRecommendations, UsersInteractions
from utils.utils import backoff

logger = logging.getLogger(__name__)


class RecommendationService:
    def __init__(
        self,
        user_data_provider: IUserDataProvider,
        recommendation_storage_provider: IRecommendationStorageProvider,
        personal_recommendations_provider: IPersonalRecommendationsProvider,
    ):
        self.user_data_provider = user_data_provider
        self.recommendation_storage_provider = recommendation_storage_provider
        self.personal_recommendations_provider = personal_recommendations_provider

    @backoff()
    async def create_recommendations(self):
        logger.info("Выгрузка информации о пользовательских действиях")
        keys = self.user_data_provider.search()
        values = self.user_data_provider.mget(keys=keys)

        interactions = []

        for key, value in zip(keys, values):
            interactions.append(
                {"user_id": key.split(":")[0], "movie_id": key.split(":")[1], "interaction": value}
            )

        logger.info("Формирования персональных рекомендаций фильмов c помощью ML сервиса")
        personals_recommendations = await self.personal_recommendations_provider.personal(
            data=UsersInteractions(
                **{
                    "factors": personal_recommendations_settings.factors,
                    "regularization": personal_recommendations_settings.regularization,
                    "iterations": personal_recommendations_settings.iterations,
                    "recommendation_count": personal_recommendations_settings.recommendation_count,
                    "interactions": interactions,
                }
            ).transform()
        )

        logger.info("Загрузка рассчитанных рекомендаций в хранилище")
        for personal_recommendations in personals_recommendations:
            filters, value = PersonalRecommendations(**personal_recommendations).transform()
            self.recommendation_storage_provider.update(filters=filters, value=value)

        logger.info("Персональные рекомендации успешно рассчитаны и сохранены в хранилище")


def get_recommendation_service():
    return RecommendationService(
        user_data_provider=get_user_data_provider(),
        recommendation_storage_provider=get_recommendation_storage_provider(),
        personal_recommendations_provider=get_personal_recommendations_provider(),
    )
