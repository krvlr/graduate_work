import logging

from core.config import (
    base_settings,
    elastic_settings,
    mongo_settings,
    movies_preprocessor_settings,
    similar_movies_settings,
)
from db.movies_preprocessor_provider import (
    IMoviesPreprocessorProvider,
    get_movies_preprocessing_provider,
)
from db.movies_storage_provider import (
    IMoviesStorageProvider,
    ObjectName,
    get_movies_storage_provider,
)
from db.recommendation_storage_provider import (
    IRecommendationStorageProvider,
    get_recommendation_storage_provider,
)
from db.similar_movies_provider import ISimilarMoviesProvider, get_similar_movies_provider
from models.movie import ElasticMovie, Movie, SimilarMovies, VectorizedMovies
from utils.utils import backoff

logger = logging.getLogger(__name__)


class RecommendationService:
    def __init__(
        self,
        movies_storage_provider: IMoviesStorageProvider,
        recommendation_storage_provider: IRecommendationStorageProvider,
        movies_preprocessing_provider: IMoviesPreprocessorProvider,
        similar_movies_provider: ISimilarMoviesProvider,
    ):
        self.movies_storage_provider = movies_storage_provider
        self.recommendation_storage_provider = recommendation_storage_provider
        self.movies_preprocessing_provider = movies_preprocessing_provider
        self.similar_movies_provider = similar_movies_provider

    @backoff()
    async def create_recommendations(self):
        logger.info("Выгрузка фильмов и векторизация их описаний с помощью сервиса NLP")

        vectorized_movies = []

        async for movies in self.movies_storage_provider.get_batch_extractor(
            obj_name=ObjectName.MOVIES,
            model=ElasticMovie,
            page_size=int(base_settings.elastic_batch_size),
        ):
            vectorized_movies.extend(
                await self.movies_preprocessing_provider.vectorize(
                    data=[Movie(**movie.dict()).transform() for movie in movies]
                )
            )

        logger.info("Формирования рекомендаций похожих фильмов c помощью ML сервиса")
        nearest_neighbours_movies = await self.similar_movies_provider.nearest_neighbours(
            data=VectorizedMovies(
                **{
                    "radius": float(similar_movies_settings.radius),
                    "n_neighbors": int(similar_movies_settings.n_neighbors),
                    "metric": similar_movies_settings.metric,
                    "documents": vectorized_movies,
                }
            ).transform()
        )

        logger.info("Загрузка рассчитанных рекомендаций в хранилище")
        for similar_movies in nearest_neighbours_movies:
            filters, value = SimilarMovies(**similar_movies).transform()
            self.recommendation_storage_provider.update(filters=filters, value=value)

        logger.info("Рекоммендации похожих фильмов успешно рассчитаны и сохранены в хранилище")


def get_recommendation_service():
    return RecommendationService(
        movies_storage_provider=get_movies_storage_provider(),
        recommendation_storage_provider=get_recommendation_storage_provider(),
        movies_preprocessing_provider=get_movies_preprocessing_provider(),
        similar_movies_provider=get_similar_movies_provider(),
    )
