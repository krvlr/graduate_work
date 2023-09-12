from fastapi import APIRouter

from models.film import FilmBrief

router = APIRouter()


@router.get("/new_movies", response_model=list[FilmBrief])
async def get_new_movies():
    return {}


@router.get("/popular_movies", response_model=list[FilmBrief])
async def get_popular_movies():
    return {}


@router.get("/", response_model=list[FilmBrief])
async def get_general_recommended_movies():
    return {}
