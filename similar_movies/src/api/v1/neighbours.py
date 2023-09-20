import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from models.document import NearestNeighboursResponse, ProcessedDocumentsRequest
from services.similarity_service import SimilarityService, get_similarity_service

logger = logging.getLogger(__name__)


router = APIRouter()


@router.post(
    "/nearest_neighbours",
    status_code=status.HTTP_200_OK,
    response_model=list[NearestNeighboursResponse],
)
async def nearest_neighbours(
    processed_documents: ProcessedDocumentsRequest,
    similarity_service: Annotated[SimilarityService, Depends(get_similarity_service)],
) -> list[NearestNeighboursResponse]:
    nearest_documents = similarity_service.transform(
        radius=processed_documents.radius,
        n_neighbors=processed_documents.n_neighbors,
        metric=processed_documents.metric,
        documents=processed_documents.documents,
    )
    return nearest_documents
