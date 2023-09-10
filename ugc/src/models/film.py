from pydantic import BaseModel
from uuid import UUID


class FilmProgress(BaseModel):
    user_id: UUID
    movie_id: UUID
    timestamp_of_film: float

    def transform(self):
        return {
            "user_id": str(self.user_id),
            "movie_id": str(self.movie_id),
            "timestamp_of_film": self.timestamp_of_film
        }
