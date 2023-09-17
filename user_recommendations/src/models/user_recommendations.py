from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class MovieSchemaRequest(BaseModel):
    movie_id: UUID


class MovieSchemaResponse(BaseModel):
    movie_id: UUID
    title: str
    imdb_rating: float
    # rating: float


class MovieSchema(BaseModel):
    id: UUID
    title: str
    imdb_rating: float

    def transform(self):
        return {"movie_id": str(self.id), "title": self.title, "imdb_rating": self.imdb_rating}


class MovieSimilarity(BaseModel):
    movie_id: UUID
    similar_movies: list[UUID]

    def transform(self):
        return self.similar_movies


class UserRecommendation(BaseModel):
    user_id: UUID
    movies_recommendations: list[UUID]

    def transform(self):
        return self.movies_recommendations
