from dataclasses import dataclass

from fastapi import Query
from orjson import orjson  # type: ignore
from pydantic import BaseModel


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = lambda v, *, default: orjson.dumps(v, default=default).decode()


class Paginator(BaseModel):
    page_number: int = Query(default=1, ge=1)
    page_size: int = Query(default=20, ge=1, le=50)


@dataclass
class FilmFilters:
    genres_id: list[str] | None = Query(default=None)
    genres_name: list[str] | None = Query(default=None)
    actors_id: list[str] | None = Query(default=None)
    actors_name: list[str] | None = Query(default=None)
    writers_id: list[str] | None = Query(default=None)
    writers_name: list[str] | None = Query(default=None)
    directors_id: list[str] | None = Query(default=None)
    directors_name: list[str] | None = Query(default=None)


class FilmPerson(BaseModel):
    id: str
    name: str


class FilmGenre(BaseModel):
    id: str
    name: str


class FilmBrief(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: float


class FilmDetail(FilmBrief):
    description: str | None
    actors: list[FilmPerson]
    writers: list[FilmPerson]
    directors: list[FilmPerson]
    genres: list[FilmGenre]


class FilmProgress(BaseModel):
    user_id: str
    movie_id: str
    timestamp_of_film: str
