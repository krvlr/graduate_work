import logging

from core.config import general_data_mongodb_settings
from db.mongodb import get_recommendations_mongodb_adapter
from models.movie import AggregatedMovieBrief

logger = logging.getLogger(__name__)


class GeneralMovieService:
    @staticmethod
    async def clear_movie_aggregation() -> None:
        await get_recommendations_mongodb_adapter().delete_all(
            general_data_mongodb_settings.collection_movies
        )

    @staticmethod
    async def save_movie_aggregation(movie: AggregatedMovieBrief) -> None:
        await get_recommendations_mongodb_adapter().insert(
            general_data_mongodb_settings.collection_movies,
            movie.model_dump(),
        )
