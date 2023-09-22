from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, fields


class Metric(Enum):
    CITYBLOCK = "cityblock"
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    MINKOWSKI = "minkowski"
    HAVERSINE = "haversine"
    L1 = "l1"
    L2 = "l2"
    MANHATTAN = "manhattan"
    NAN_EUCLIDEAN = "nan_euclidean"


class ElasticMovie(BaseModel):
    id: UUID
    description: str | None


class Movie(BaseModel):
    id: UUID
    description: str | None

    def transform(self):
        return {"id": str(self.id), "text": self.description or ""}


class VectorizedMovie(BaseModel):
    id: UUID
    embedding: list

    def transform(self):
        return {"id": str(self.id), "embedding": self.embedding}


class VectorizedMovies(BaseModel):
    radius: float
    n_neighbors: int
    metric: Metric
    documents: list[VectorizedMovie]

    class Config:
        use_enum_values = True

    def transform(self):
        return {
            "radius": self.radius,
            "n_neighbors": self.n_neighbors,
            "metric": self.metric,
            "documents": [document.transform() for document in self.documents],
        }


class SimilarMovies(BaseModel):
    id: UUID
    cosine_similarities: list[float]
    neighbours: list[UUID]

    def transform(self):
        return {"movie_id": str(self.id)}, {
            "movie_id": str(self.id),
            "similar_movies": [str(neighbour) for neighbour in self.neighbours],
        }
