import logging
from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from core.config import base_settings, mongo_settings
from db.general_recommendations_provider import (
    get_general_recommendations_provider,
    IGeneralRecommendationsProvider,
)
from db.movie_provider import IMovieProvider, get_movie_provider
from db.recommendation_provider import IRecommendationStorageProvider, get_recommendation_provider
from db.user_data_provider import IStorageUserDataProvider, get_user_data_provider
from models.user_recommendations import (
    MovieSchema,
    MovieSchemaRequest,
    MovieSimilarity,
    UserRecommendation,
    GeneralMovieSchemaResponse,
    MovieSchemaResponse,
)
from utils.utils import backoff, custom_sample

logger = logging.getLogger(__name__)


class RecommendationService:
    def __init__(
        self,
        recommendation_provider: IRecommendationStorageProvider,
        movie_provider: IMovieProvider,
        user_data_provider: IStorageUserDataProvider,
        general_recommendations_provider: IGeneralRecommendationsProvider,
    ):
        self.recommendation_provider = recommendation_provider
        self.movie_provider = movie_provider
        self.user_data_provider = user_data_provider
        self.general_recommendations_provider = general_recommendations_provider
        self.collection_user_recommendation = mongo_settings.collection_user_recommendation
        self.collection_similar_movies = mongo_settings.collection_similar_movies

    @backoff(max_count_sleep=3)
    @custom_sample(size=base_settings.user_recommendation_size)
    async def get_personal_recommendations(self, user_id: UUID):
        recommendations = await self.recommendation_provider.get(
            collection=self.collection_user_recommendation, filters={"user_id": str(user_id)}
        )
        if recommendations:
            movies = UserRecommendation(**recommendations).transform()
            detailed_recommendations = await self.get_movies_details(movies=movies)
            return detailed_recommendations

    @backoff()
    @custom_sample(size=base_settings.user_recommendation_size)
    async def get_general_recommendations(self, user_id: UUID) -> list[GeneralMovieSchemaResponse]:
        user_profile = await self.user_data_provider.get(user_id=user_id)
        preference_genres = user_profile["genres"]

        general_recommendations = self.general_recommendations_provider.get(preference_genres)

        return [GeneralMovieSchemaResponse(**movie) for movie in await general_recommendations]

    @backoff()
    async def get_movies_details(self, movies: list[UUID]):
        movies_details = []

        ratings = self.general_recommendations_provider.get_ratings(
            [str(movie_id) for movie_id in movies]
        )

        for movie_id, rating in zip(movies, ratings):
            response = await self.movie_provider.get(movie_id=movie_id)

            if response:
                movie_details = MovieSchema(rating=rating, **response).transform()
                movies_details.append(movie_details)

        return movies_details

    @staticmethod
    def convert_general_recommendations(
        movies: list[GeneralMovieSchemaResponse],
    ) -> list[MovieSchemaResponse]:
        return [
            MovieSchemaResponse(
                movie_id=movie.id,
                title=movie.title,
                imdb_rating=movie.imdb_rating,
                rating=movie.rating,
            )
            for movie in movies
        ]

    async def get_recommendations(self, user_id: UUID):
        try:
            recommendations = await self.get_personal_recommendations(user_id=user_id)
            if not recommendations:
                logger.exception(
                    f"Персональные рекомендации для пользователя с id={user_id} не найдены, "
                    f"возвращаем общие"
                )
                recommendations = self.convert_general_recommendations(
                    await self.get_general_recommendations(user_id=user_id)
                )
            return recommendations
        except Exception:
            logger.exception(
                f"Персональные рекомендации для пользователя с id={user_id} недоступны, "
                f"возвращаем общие"
            )

            return self.convert_general_recommendations(
                await self.get_general_recommendations(user_id=user_id)
            )

    @backoff()
    @custom_sample(size=base_settings.user_recommendation_size)
    async def get_similar_movies(self, movie: MovieSchemaRequest):
        recommendations = await self.recommendation_provider.get(
            collection=self.collection_similar_movies, filters={"movie_id": str(movie.movie_id)}
        )

        if recommendations:
            movies = MovieSimilarity(**recommendations).transform()
            detailed_recommendations = await self.get_movies_details(movies=movies)
            return detailed_recommendations

        return []


@lru_cache()
def get_recommendation_service(
    recommendation_provider=Depends(get_recommendation_provider),
    movie_provider=Depends(get_movie_provider),
    user_data_provider=Depends(get_user_data_provider),
    general_recommendations_provider=Depends(get_general_recommendations_provider),
):
    recommendation_service = RecommendationService(
        recommendation_provider=recommendation_provider,
        movie_provider=movie_provider,
        user_data_provider=user_data_provider,
        general_recommendations_provider=general_recommendations_provider,
    )
    return recommendation_service
