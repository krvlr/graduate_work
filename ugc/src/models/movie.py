from pydantic import BaseModel, validator
from uuid import UUID
from enum import Enum
from datetime import datetime
from fastapi import status, HTTPException


class BookmarkAction(Enum):
    ADD = "add"
    DELETE = "delete"


class ReviewScore(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


class MovieProgress(BaseModel):
    movie_id: UUID
    progress: float
    created: datetime

    def transform(self):
        return {
            "movie_id": str(self.movie_id),
            "progress": self.progress,
            "created": str(self.created),
        }


class MovieBookmark(BaseModel):
    movie_id: UUID
    action: BookmarkAction
    created: datetime

    class Config:
        use_enum_values = True

    def transform(self):
        return {
            "movie_id": str(self.movie_id),
            "progress": self.action,
            "created": str(self.created),
        }


class MovieReview(BaseModel):
    movie_id: UUID
    action: str
    description: str
    score: ReviewScore
    created: datetime

    class Config:
        use_enum_values = True

    def transform(self):
        return {
            "movie_id": str(self.movie_id),
            "action": self.action,
            "description": self.description,
            "score": self.score,
            "created": str(self.created),
        }


class MovieRating(BaseModel):
    movie_id: UUID
    rating: int
    created: datetime

    def transform(self):
        return {"movie_id": str(self.movie_id), "rating": self.rating, "created": str(self.created)}

    @validator("rating")
    @classmethod
    def validate_rating(cls, value):
        if value > 10:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Ошибка валидации. Рейтинг не может быть больше 10.",
            )