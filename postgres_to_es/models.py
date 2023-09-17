from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class ESFilmworkPersonData(BaseModel):
    id: str
    name: str


class ESFilmworkGenreData(BaseModel):
    id: str
    name: str


class ESFilmworkData(BaseModel):
    id: str
    imdb_rating: Optional[float]
    title: str
    description: Optional[str]
    actors_names: list[str] = []
    writers_names: list[str] = []
    directors_names: list[str] = []
    actors: list[ESFilmworkPersonData] = []
    writers: list[ESFilmworkPersonData] = []
    directors: list[ESFilmworkPersonData] = []
    genres: list[ESFilmworkGenreData] = []
    creation_date: Optional[datetime] = None

    @validator("creation_date", pre=True)
    def parse_creation_date(cls, value):
        return datetime.combine(value, datetime.min.time())


class ESPersonFilmworkData(BaseModel):
    id: str
    roles: list[str] = []


class ESPersonData(BaseModel):
    id: str
    full_name: str
    films: list[ESPersonFilmworkData] = []


class ESGenreData(BaseModel):
    id: str
    name: str
    description: str | None
