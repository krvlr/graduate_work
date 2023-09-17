import random

from fastapi import APIRouter, Query, Depends
from models.movie import AggregatedMovieBrief
from services.general_recommendations_service import (
    get_general_recommendation_service,
    GeneralRecommendationsService,
)

router = APIRouter()


@router.get("/new", response_model=list[AggregatedMovieBrief])
async def get_new_movies(
    limit: int = Query(default=10, ge=0),
    service: GeneralRecommendationsService = Depends(get_general_recommendation_service),
):
    latest_movies = await service.get_new_movies(limit)
    random.shuffle(latest_movies)
    return latest_movies


@router.get("/popular", response_model=list[AggregatedMovieBrief])
async def get_popular_movies(
    limit: int = Query(default=10, ge=0),
    service: GeneralRecommendationsService = Depends(get_general_recommendation_service),
):
    popular_movies = await service.get_popular_movies(limit)
    random.shuffle(popular_movies)
    return popular_movies


@router.get("/replacement", response_model=list[AggregatedMovieBrief])
async def get_replacement_movies(
    limit: int = Query(default=10, ge=0),
    genres: list[str] = Query(default=None),
    service: GeneralRecommendationsService = Depends(get_general_recommendation_service),
):
    replacement_movies = await service.get_replacement_recommendations(limit, genres)
    random.shuffle(replacement_movies)
    return replacement_movies
