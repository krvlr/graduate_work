import logging
from typing import Annotated

import pandas as pd
import scipy.sparse as scs
from implicit.als import AlternatingLeastSquares
from models.user import UserInteractions

logger = logging.getLogger(__name__)


class RecommendationService:
    @staticmethod
    def transform(
        factors: int,
        regularization: float,
        iterations: int,
        recommendation_count: int,
        interactions: UserInteractions,
    ) -> list[dict]:
        user_item = pd.DataFrame([interaction.transform() for interaction in interactions])

        user_ids = user_item["user_id"].unique()
        movie_ids = user_item["movie_id"].unique()

        user_id2idx = dict(zip(user_ids, range(len(user_ids))))
        movie_id2idx = dict(zip(movie_ids, range(len(movie_ids))))

        user_item["user_index"] = user_item["user_id"].map(user_id2idx)
        user_item["movie_index"] = user_item["movie_id"].map(movie_id2idx)

        sparse_user_item = scs.csr_matrix(
            (user_item["interaction"], (user_item["user_index"], user_item["movie_index"]))
        )

        logger.info(
            f"Обучение ALS с factors = {factors}, regularization = {regularization}, iterations = {iterations}"
        )

        als = AlternatingLeastSquares(
            factors=factors, regularization=regularization, iterations=iterations
        )
        als.fit(sparse_user_item)

        item_indexes, scores = als.recommend(
            list(range(len(user_ids))), sparse_user_item, recommendation_count
        )

        personal_recommendations = []

        for user_index in range(len(user_ids)):
            personal_recommendations.append(
                {
                    "user_id": user_ids[user_index],
                    "movies_recommendations": movie_ids[item_indexes[user_index]].tolist(),
                }
            )

        return personal_recommendations


def get_recommendation_service() -> RecommendationService:
    return RecommendationService()
