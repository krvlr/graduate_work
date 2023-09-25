import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from models.user import PersonalRecommendationResponse, UsersInteractionsRequest
from services.recommendation_service import RecommendationService, get_recommendation_service

logger = logging.getLogger(__name__)


router = APIRouter()


@router.post(
    "/personal",
    status_code=status.HTTP_200_OK,
    response_model=list[PersonalRecommendationResponse],
)
async def personal(
    users_interactions: UsersInteractionsRequest,
    recommendation_service: Annotated[RecommendationService, Depends(get_recommendation_service)],
) -> list[PersonalRecommendationResponse]:
    personals_recommendations = recommendation_service.transform(
        factors=users_interactions.factors,
        regularization=users_interactions.regularization,
        iterations=users_interactions.iterations,
        recommendation_count=users_interactions.recommendation_count,
        interactions=users_interactions.interactions,
    )
    return personals_recommendations
