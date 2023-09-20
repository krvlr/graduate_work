import logging
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Optional

import pymongo
from fastapi import Depends

from core.config import general_data_mongodb_settings
from db.mongodb import get_mongodb_adapter, MongodbAdapter
from models.movie import AggregatedMovieBrief

logger = logging.getLogger(__name__)


class GeneralRecommendationsService:
    def __init__(self, mongodb_adapter: MongodbAdapter):
        self.mongodb_adapter = mongodb_adapter

    async def get_new_movies(self, limit: int) -> list[AggregatedMovieBrief]:
        return [
            AggregatedMovieBrief(**movie)
            for movie in await self.mongodb_adapter.find(
                collection=general_data_mongodb_settings.collection_movies,
                filters={},
                limit=limit,
                offset=0,
                sort="creation_date",
                direction=pymongo.DESCENDING,
            )
        ]

    async def get_popular_movies(self, limit: int) -> list[AggregatedMovieBrief]:
        return [
            AggregatedMovieBrief(**movie)
            for movie in await self.mongodb_adapter.find(
                collection=general_data_mongodb_settings.collection_movies,
                filters={},
                limit=limit,
                offset=0,
                sort="rating",
                direction=pymongo.DESCENDING,
            )
        ]

    async def get_replacement_recommendations(
        self, limit: int, genres: Optional[list[str]] = None
    ) -> list[AggregatedMovieBrief]:
        genres_filter = dict()
        if genres:
            genres_filter = {"genres.name": {"$in": genres}}

        start_date_filter = datetime.now() - timedelta(days=365)
        return [
            AggregatedMovieBrief(**movie)
            for movie in await self.mongodb_adapter.find(
                collection=general_data_mongodb_settings.collection_movies,
                filters={"creation_date": {"$gte": start_date_filter}} | genres_filter,
                limit=limit,
                offset=0,
                sort="rating",
                direction=pymongo.DESCENDING,
            )
        ]


@lru_cache
def get_general_recommendation_service(
    mongodb_adapter=Depends(get_mongodb_adapter),
) -> GeneralRecommendationsService:
    return GeneralRecommendationsService(mongodb_adapter=mongodb_adapter)
