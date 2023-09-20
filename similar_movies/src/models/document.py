from enum import Enum
from uuid import UUID

from fastapi import HTTPException, status
from pydantic import BaseModel, validator


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


class ProcessedDocument(BaseModel):
    id: UUID
    embedding: list


class ProcessedDocumentsRequest(BaseModel):
    radius: float
    n_neighbors: int
    metric: Metric
    documents: list[ProcessedDocument]

    class Config:
        use_enum_values = True

    @validator("radius")
    @classmethod
    def validate_radius(cls, value):
        if value > 1.0 or value < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Ошибка валидации. Радиус должен быть в интервале от 0 до 1.0.",
            )
        return value


class NearestNeighboursResponse(BaseModel):
    id: UUID
    cosine_similarities: list[float]
    neighbours: list[UUID]
