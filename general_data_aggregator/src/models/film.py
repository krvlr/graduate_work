from orjson import orjson  # type: ignore
from pydantic import BaseModel


class FilmPerson(BaseModel):
    id: str
    name: str


class FilmGenre(BaseModel):
    id: str
    name: str


class FilmBrief(BaseModel):
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
