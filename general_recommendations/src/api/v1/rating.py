from fastapi import APIRouter, Query, Depends

from services.rating_service import get_rating_service, RatingService

router = APIRouter()


@router.get("/ratings", response_model=list[float])
async def get_movies_ratings(
    movies_ids: list[str] = Query(default=None),
    service: RatingService = Depends(get_rating_service),
):
    return await service.get_movies_ratings(movies_ids)
