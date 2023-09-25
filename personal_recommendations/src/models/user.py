from uuid import UUID

from pydantic import BaseModel


class UserInteractions(BaseModel):
    user_id: UUID
    movie_id: UUID
    interaction: float

    def transform(self):
        return {
            "user_id": str(self.user_id),
            "movie_id": str(self.movie_id),
            "interaction": self.interaction,
        }


class UsersInteractionsRequest(BaseModel):
    factors: int
    regularization: float
    iterations: int
    recommendation_count: int
    interactions: list[UserInteractions]


class PersonalRecommendationResponse(BaseModel):
    user_id: UUID
    movies_recommendations: list[UUID]
