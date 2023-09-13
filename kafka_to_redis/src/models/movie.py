from pydantic import BaseModel, validator
from uuid import UUID
from datetime import datetime


class MovieProgress(BaseModel):
    movie_id: UUID
    user_id: UUID
    progress: float
    created: datetime

    def get_key(self):
        return f"{str(self.user_id)}:{str(self.movie_id)}:progress"

    def transform(self):
        return self.get_key(), self.progress


class MovieBookmark(BaseModel):
    movie_id: UUID
    user_id: UUID
    action: str
    created: datetime

    def get_key(self):
        return f"{str(self.user_id)}:{str(self.movie_id)}:bookmark"

    def transform(self):
        return self.get_key(), self.action


class MovieReview(BaseModel):
    movie_id: UUID
    user_id: UUID
    summary: str
    description: str
    score: str
    created: datetime

    def get_key(self):
        return f"{str(self.user_id)}:{str(self.movie_id)}:review"

    def transform(self):
        return self.get_key(), self.score


class MovieRating(BaseModel):
    movie_id: UUID
    user_id: UUID
    rating: int
    created: datetime

    def get_key(self):
        return f"{str(self.user_id)}:{str(self.movie_id)}:rating"

    def transform(self) -> tuple:
        return self.get_key(), self.rating
