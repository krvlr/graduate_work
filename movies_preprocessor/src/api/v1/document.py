import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from models.document import DocumentRequest, ProcessedDocumentResponse
from services.vectorize_service import VectorizeService, get_vectorize_service

logger = logging.getLogger(__name__)


router = APIRouter()


@router.post(
    "/vectorize", status_code=status.HTTP_200_OK, response_model=list[ProcessedDocumentResponse]
)
async def vectorize(
    documents: list[DocumentRequest],
    vectorize_service: Annotated[VectorizeService, Depends(get_vectorize_service)],
) -> list[ProcessedDocumentResponse]:
    processed_texts = vectorize_service.transform(documents=documents)
    return processed_texts
