import logging.config

from core.config import kafka_settings, redis_settings

from models.movie import MovieProgress, MovieBookmark, MovieReview, MovieRating

from utils.extract import KafkaExtractor, Extractor
from utils.transform import DataTransformer, Transformer
from utils.load import Loader, RedisLoader

from confluent_kafka.cimpl import Consumer
from confluent_kafka.admin import AdminClient

from core.logger import LOGGER_CONFIG

from redis import Redis
from db.storage_provider import StorageRedisProvider

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


def etl(extrator: Extractor, transformer: Transformer, loader: Loader):
    logger.info("Start etl from Kafka to Redis")
    batch_extractor = extrator.get_batch_extractor(
        batch_size=int(kafka_settings.num_messages), timeout=int(kafka_settings.timeout)
    )
    batch_transformer = transformer.get_batch_transformer(batch_extractor=batch_extractor)
    loader.save_data(batch_transformer)


def main():
    logger.info("Start main")

    kafka_extractor = KafkaExtractor(
        consumer=Consumer(kafka_settings.get_kafka_config()),
        admin_client=AdminClient(kafka_settings.get_kafka_config()),
        topics=kafka_settings.get_topics(),
    )
    data_transformer = DataTransformer(
        topic_to_model={
            kafka_settings.movies_topic: MovieProgress,
            kafka_settings.bookmarks_topic: MovieBookmark,
            kafka_settings.reviews_topic: MovieReview,
            kafka_settings.ratings_topic: MovieRating,
        }
    )
    redis_loader = RedisLoader(
        storage=StorageRedisProvider(
            redis=Redis(host=redis_settings.redis_host, port=redis_settings.redis_port)
        )
    )

    while True:
        try:
            etl(extrator=kafka_extractor, transformer=data_transformer, loader=redis_loader)
        except Exception as ex:
            logger.error(f"Error etl data from Kafka to Redis: {ex}")


if __name__ == "__main__":
    main()
