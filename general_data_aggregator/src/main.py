import asyncio
import datetime
import logging.config

from elasticsearch import AsyncElasticsearch
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import (
    sources_elastic_settings,
    sources_mongodb_settings,
    general_data_mongodb_settings,
    base_settings,
)
from core.logger import LOGGER_CONFIG
from db import elastic, mongodb
from db.elastic import ObjectName
from models.movie import ElasticMovieBrief, AggregatedMovieBrief
from services.general_movie_service import GeneralMovieService
from services.rating_service import RatingService

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


def startup():
    elastic.client = AsyncElasticsearch(
        hosts=[f"{sources_elastic_settings.host}:{sources_elastic_settings.port}"]
    )
    mongodb.source_client = AsyncIOMotorClient(
        f"mongodb://{sources_mongodb_settings.login}:{sources_mongodb_settings.password}@"
        f"{sources_mongodb_settings.host}:{sources_mongodb_settings.port}/"
        f"?authSource={sources_mongodb_settings.mongo_db_name}&authMechanism=SCRAM-SHA-256"
    )

    mongodb.recommendations_client = AsyncIOMotorClient(
        f"mongodb://{general_data_mongodb_settings.login}:{general_data_mongodb_settings.password}@"
        f"{general_data_mongodb_settings.host}:{general_data_mongodb_settings.port}/"
        f"?authSource={general_data_mongodb_settings.mongo_db_name}&authMechanism=SCRAM-SHA-256"
    )


async def shutdown():
    await elastic.client.close()
    mongodb.source_client.close()
    mongodb.recommendations_client.close()


async def main():
    startup()

    try:
        await GeneralMovieService.clear_movie_aggregation()

        page = 0
        while True:
            movies = await elastic.get_elastic_adapter().search(
                obj_name=ObjectName.MOVIES,
                model=ElasticMovieBrief,
                page_number=page,
                page_size=base_settings.batch_size,
            )
            page += 1

            if len(movies) == 0:
                break

            for movie in movies:  # type: ElasticMovieBrief
                rating = await RatingService.get_avg_ratings_of_movie(movie.id)

                # используем внешний рейтинг (imdb), если собственный не заполнен (0)
                rating = rating if rating else movie.imdb_rating if movie.imdb_rating else 0

                await GeneralMovieService.save_movie_aggregation(
                    AggregatedMovieBrief(rating=rating, **movie.model_dump())
                )
    except Exception:
        logger.exception("Ошибка агрегации данных общих рекомендаций")
    finally:
        await shutdown()


if __name__ == "__main__":
    logger.info(f"Запуск агрегатора данных общих рекомендаций {datetime.datetime.now()}")

    asyncio.run(main())

    logger.info("Завершение работы агрегатора данных общих рекомендаций")
