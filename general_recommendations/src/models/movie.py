from datetime import datetime
from typing import Optional

from pydantic import BaseModel, fields


class FilmGenre(BaseModel):
    id: str
    name: str


class AggregatedMovieBrief(BaseModel):
    id: str
    title: str
    imdb_rating: float | None = fields.Field(default=0)
    creation_date: Optional[datetime] = None
    genres: list[FilmGenre]
    rating: float
