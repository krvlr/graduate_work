import logging
from functools import lru_cache
from uuid import UUID, uuid4

from core.config import base_settings, mongo_settings
from db.movie_provider import IMovieProvider, get_movie_provider
from db.recommendation_provider import IRecommendationStorageProvider, get_recommendation_provider
from db.user_data_provider import IStorageUserDataProvider, get_user_data_provider
from fastapi import Depends
from models.user_recommendations import (
    MovieSchema,
    MovieSchemaRequest,
    MovieSimilarity,
    UserRecommendation,
)
from utils.utils import backoff, custom_sample

logger = logging.getLogger(__name__)


class RecommendationService:
    def __init__(
        self,
        recommendation_provider: IRecommendationStorageProvider,
        movie_provider: IMovieProvider,
        user_data_provider: IStorageUserDataProvider,
        # common_recommendation_provider
    ):
        self.recommendation_provider = recommendation_provider
        self.movie_provider = movie_provider
        self.user_data_provider = user_data_provider
        # self.common_recommendation_provider = common_recommendation_provider
        self.collection_user_recommendation = mongo_settings.collection_user_recommendation
        self.collection_similar_movies = mongo_settings.collection_similar_movies

    @backoff()
    @custom_sample(size=int(base_settings.user_recommendation_size))
    async def get_personal_recommendations(self, user_id: UUID):
        recommendations = await self.recommendation_provider.get(
            collection=self.collection_user_recommendation, filters={"user_id": str(user_id)}
        )
        if recommendations:
            movies = UserRecommendation(**recommendations).transform()
            detailed_recommendations = await self.get_movies_details(movies=movies)
            return detailed_recommendations

    @backoff()
    @custom_sample(size=int(base_settings.user_recommendation_size))
    async def get_common_recommendations(self, user_id: UUID):
        pass
        # user_profile = await self.user_data_provider.get(user_id=user_id)
        # preference_genres = user_profile['genres']
        # TODO: получение общих рекоммендации и их (возможная) фильтрация

    @backoff()
    async def get_movies_details(self, movies: list[UUID]):
        movies_details = []

        for movie_id in movies:
            response = await self.movie_provider.get(movie_id=movie_id)

            if response:
                movie_details = MovieSchema(**response).transform()
                movies_details.append(movie_details)

        return movies_details

    async def get_recommendations(self, user_id: UUID):
        recommendations = await self.get_personal_recommendations(user_id=user_id)

        if not recommendations:
            # recommendations = await self.get_common_recommendations(user_id=user_id)
            return []

        return recommendations

    @backoff()
    @custom_sample(size=int(base_settings.user_recommendation_size))
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
    # common_recommendation_provider=Depends(get_common_recommendation_provider),
):
    recommendation_service = RecommendationService(
        recommendation_provider=recommendation_provider,
        movie_provider=movie_provider,
        user_data_provider=user_data_provider,
        # common_recommendation_provider=common_recommendation_provider
    )
    return recommendation_service
