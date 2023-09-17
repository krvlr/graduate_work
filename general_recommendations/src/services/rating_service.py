import logging
from functools import lru_cache

from fastapi import Depends

from core.config import general_data_mongodb_settings
from db.mongodb import get_mongodb_adapter, MongodbAdapter

logger = logging.getLogger(__name__)


class RatingService:
    def __init__(self, mongodb_adapter: MongodbAdapter):
        self.mongodb_adapter = mongodb_adapter

    async def get_movies_ratings(self, movies_ids: list[str]) -> list[float]:
        movie_rating = {
            movie.get("id"): movie.get("rating")
            for movie in await self.mongodb_adapter.find(
                collection=general_data_mongodb_settings.collection_movies,
                filters={"id": {"$in": movies_ids}},
                limit=1000,
                offset=0,
            )
        }
        return [movie_rating.get(move_id, 0) for move_id in movies_ids]


@lru_cache
def get_rating_service(
    mongodb_adapter=Depends(get_mongodb_adapter),
) -> RatingService:
    return RatingService(mongodb_adapter=mongodb_adapter)
