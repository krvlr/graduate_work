import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from models.user_recommendations import MovieSchemaRequest, MovieSchemaResponse
from services.auth_service import JWTBearerService, get_jwt_bearer_service
from services.user_recommendations import RecommendationService, get_recommendation_service

logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/personal", status_code=status.HTTP_200_OK, response_model=list[MovieSchemaResponse])
async def personal(
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())],
    recommendation_service: Annotated[RecommendationService, Depends(get_recommendation_service)],
) -> dict:
    recommendation_movies = await recommendation_service.get_recommendations(user_id=user_id)
    return recommendation_movies


@router.post(
    "/similar",
    dependencies=[Depends(JWTBearerService())],
    response_model=list[MovieSchemaResponse],
    status_code=status.HTTP_200_OK,
)
async def similar(
    movie: MovieSchemaRequest,
    recommendation_service: Annotated[RecommendationService, Depends(get_recommendation_service)],
) -> dict:
    similar_movies = await recommendation_service.get_similar_movies(movie=movie)
    return similar_movies
