import logging
import re
from abc import ABC, abstractmethod

import numpy as np
from fastapi import Depends
from gensim.models import KeyedVectors

logger = logging.getLogger(__name__)


wv: KeyedVectors | None = None
weights: dict | None = None


def get_wv():
    return wv


def get_weights():
    return weights


class IVectorizer(ABC):
    @abstractmethod
    def vectorize_texts(self, texts: list[str]):
        pass


class MeanEmbeddingVectorizer(IVectorizer):
    def __init__(
        self,
        wv: KeyedVectors,
        weights: dict,
    ):
        self.wv = wv
        self.weights = weights
        self.vocab = set(self.wv.index_to_key)

    def vectorize_text(self, text: str):
        text_weights = [self.weights.get(tok, 1) for tok in text.split() if tok in self.vocab]
        embeddings = [self.wv[tok] for tok in text.split() if tok in self.vocab]

        if text_weights:
            embedding = np.average(a=embeddings, axis=0, weights=text_weights)
            return embedding

        return np.zeros(self.wv.vector_size)

    def vectorize_texts(self, texts: list[str]):
        logger.info("Start vectorize preprocessed texts")
        return [self.vectorize_text(text) for text in texts]


def get_vectorizer(wv=Depends(get_wv), weights=Depends(get_weights)):
    vectorizer = MeanEmbeddingVectorizer(
        wv=wv,
        weights=weights,
    )
    return vectorizer
