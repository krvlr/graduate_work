import datetime
import logging.config

from elasticsearch import AsyncElasticsearch
from motor.motor_asyncio import AsyncIOMotorClient

from core.logger import LOGGER_CONFIG
from core.config import (
    sources_elastic_settings,
    sources_mongodb_settings,
)
from db import sources_elastic, sources_mongodb

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info(f"Запуск агрегатора данных общих рекомендаций {datetime.datetime.now()}")

    # sources_elastic.client = AsyncElasticsearch(
    #     hosts=[f"{sources_elastic_settings.host}:{sources_elastic_settings.port}"]
    # )
    # sources_mongodb.client = AsyncIOMotorClient(
    #     f"mongodb://{sources_mongodb_settings.login}:{sources_mongodb_settings.password}@"
    #     f"{sources_mongodb_settings.mongodb_host}:{sources_mongodb_settings.mongodb_port}/"
    #     f"?authSource={sources_mongodb_settings.mongo_db_name}&authMechanism=SCRAM-SHA-256"
    # )

    logger.info("Завершение работы агрегатора данных общих рекомендаций")
