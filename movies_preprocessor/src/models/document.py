from uuid import UUID

from pydantic import BaseModel


class DocumentRequest(BaseModel):
    id: UUID
    text: str


class ProcessedDocumentResponse(BaseModel):
    id: UUID
    processed_text: str
    embedding: list
