import logging

from core.config import kafka_settings
from models.movie import MovieProgress, MovieBookmark, MovieReview, MovieRating
from db.base_db import QueueProvider
from services.auth_service import get_jwt_bearer_service
from services.ugc_service import UGCService, get_ugc_service
from typing import Annotated
from fastapi.security import HTTPBearer

from fastapi import APIRouter, Depends

logger = logging.getLogger(__name__)


router = APIRouter()


@router.put("/register_movie_progress")
async def register_movie_progress(
    film_progress: MovieProgress,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())],
):
    await ugc_service.register_event(
        topic=kafka_settings.movies_topic,
        event=film_progress.transform() | {"user_id": user_id},
        key=f"{user_id}-{film_progress.movie_id}",
    )
    return {"status": "OK"}


@router.put("/register_bookmark")
async def register_bookmark(
    bookmark: MovieBookmark,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())],
):
    await ugc_service.register_event(
        topic=kafka_settings.bookmarks_topic,
        event=bookmark.transform() | {"user_id": user_id},
        key=f"{user_id}-{bookmark.movie_id}",
    )
    return {"status": "OK"}


@router.put("/register_review")
async def register_review(
    review: MovieReview,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())],
):
    await ugc_service.register_event(
        topic=kafka_settings.reviews_topic,
        event=review.transform() | {"user_id": user_id},
        key=f"{user_id}-{review.movie_id}",
    )
    return {"status": "OK"}


@router.put("/register_rating")
async def register_rating(
    rating: MovieRating,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())],
):
    await ugc_service.register_event(
        topic=kafka_settings.ratings_topic,
        event=rating.transform() | {"user_id": user_id},
        key=f"{user_id}-{rating.movie_id}",
    )
    return {"status": "OK"}
