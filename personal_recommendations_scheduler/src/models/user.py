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


class UsersInteractions(BaseModel):
    factors: int
    regularization: float
    iterations: int
    recommendation_count: int
    interactions: list[UserInteractions]

    def transform(self):
        return {
            "factors": self.factors,
            "regularization": self.regularization,
            "iterations": self.iterations,
            "recommendation_count": self.recommendation_count,
            "interactions": [interaction.transform() for interaction in self.interactions],
        }


class PersonalRecommendations(BaseModel):
    user_id: UUID
    movies_recommendations: list[UUID]

    def transform(self):
        return {"user_id": str(self.user_id)}, {
            "user_id": str(self.user_id),
            "movies_recommendations": [str(movie_id) for movie_id in self.movies_recommendations],
        }
