import logging
from typing import Annotated

import numpy as np
from models.document import ProcessedDocument
from sklearn.neighbors import NearestNeighbors

logger = logging.getLogger(__name__)


class SimilarityService:
    @staticmethod
    def transform(radius: float, n_neighbors: int, metric: str, documents: ProcessedDocument):
        n_neighbors = min(n_neighbors, len(documents)) + 1

        document_ids = np.array([document.id for document in documents])
        embeddings = [document.embedding for document in documents]

        logger.info(
            f"Fit model NearestNeighbors with radius = {radius}, n_neighbors = {n_neighbors}, metric = {metric}"
        )
        nn = NearestNeighbors(radius=radius, n_neighbors=n_neighbors, metric=metric)
        nn.fit(embeddings)

        logger.info("Calculate nearest neighbors")
        prediction_distances, prediction_indexes = nn.kneighbors(embeddings)

        nearest_documents = []

        for index in range(len(document_ids)):
            mask = prediction_indexes[index] != index

            indexes = prediction_indexes[index][mask]
            distances = prediction_distances[index][mask]

            neighbours = document_ids[indexes]

            nearest_documents.append(
                {
                    "id": document_ids[index],
                    "cosine_similarities": list(map(lambda x: 1 - x, distances)),
                    "neighbours": list(neighbours),
                }
            )

        return nearest_documents


def get_similarity_service() -> SimilarityService:
    return SimilarityService()
