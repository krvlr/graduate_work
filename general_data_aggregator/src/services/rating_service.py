import logging

from core.config import sources_mongodb_settings
from db.mongodb import get_source_mongodb_adapter

logger = logging.getLogger(__name__)


class RatingService:
    @staticmethod
    async def get_avg_ratings_of_movie(movie_id: str) -> float | None:
        pipeline = [
            {"$match": {"film_id": movie_id}},
            {"$group": {"_id": "@film_id", "avg_score": {"$avg": "$rating_score"}}},
        ]
        return await get_source_mongodb_adapter().avg(
            sources_mongodb_settings.collection_rating, pipeline
        )
