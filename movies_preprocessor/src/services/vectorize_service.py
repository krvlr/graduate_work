import logging
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from models.document import DocumentRequest
from utils.preprocessor import IPreprocessor, get_preprocessor
from utils.vectorizer import IVectorizer, get_vectorizer

logger = logging.getLogger(__name__)


class VectorizeService:
    def __init__(self, preprocessor: IPreprocessor, vectorizer: IVectorizer):
        self.preprocessor = preprocessor
        self.vectorizer = vectorizer

    def transform(self, documents: list[DocumentRequest]) -> list[dict]:
        texts = [document.text for document in documents]
        processed_texts = self.preprocessor.process_texts(texts=texts)
        vectorized_tests = self.vectorizer.vectorize_texts(texts=processed_texts)
        logger.info("Success finish preprocess and vectorize texts")
        return [
            {"id": documents[i].id, "processed_text": text, "embedding": list(embedding)}
            for i, (text, embedding) in enumerate(zip(processed_texts, vectorized_tests))
        ]


def get_vectorize_service(
    preprocessor=Depends(get_preprocessor), vectorizer=Depends(get_vectorizer)
) -> VectorizeService:
    vectorize_service = VectorizeService(preprocessor=preprocessor, vectorizer=vectorizer)
    return vectorize_service
