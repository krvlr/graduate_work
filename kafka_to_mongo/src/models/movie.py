from datetime import datetime
from uuid import UUID

from core.config import mongo_settings
from pydantic import BaseModel, validator


class MovieProgress(BaseModel):
    movie_id: UUID
    user_id: UUID
    progress: float
    created: datetime

    def transform(self):
        return (
            mongo_settings.collection_progress,
            {
                "user_id": str(self.user_id),
                "movie_id": str(self.movie_id),
            },
            {
                "user_id": str(self.user_id),
                "movie_id": str(self.movie_id),
                "progress": self.progress,
            },
        )


class MovieBookmark(BaseModel):
    movie_id: UUID
    user_id: UUID
    action: str
    created: datetime

    def transform(self):
        return (
            mongo_settings.collection_bookmark,
            {
                "user_id": str(self.user_id),
                "movie_id": str(self.movie_id),
            },
            {
                "user_id": str(self.user_id),
                "movie_id": str(self.movie_id),
                "action": self.action,
            },
        )


class MovieReview(BaseModel):
    movie_id: UUID
    user_id: UUID
    summary: str
    description: str
    score: str
    created: datetime

    def transform(self):
        return (
            mongo_settings.collection_review,
            {
                "user_id": str(self.user_id),
                "movie_id": str(self.movie_id),
            },
            {
                "user_id": str(self.user_id),
                "movie_id": str(self.movie_id),
                "score": self.score,
            },
        )


class MovieRating(BaseModel):
    movie_id: UUID
    user_id: UUID
    rating: int
    created: datetime

    def transform(self):
        return (
            mongo_settings.collection_rating,
            {
                "user_id": str(self.user_id),
                "movie_id": str(self.movie_id),
            },
            {
                "user_id": str(self.user_id),
                "movie_id": str(self.movie_id),
                "rating": self.rating,
            },
        )
