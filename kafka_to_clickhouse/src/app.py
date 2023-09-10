import logging.config

from core.config import kafka_settings, clickhouse_settings

from utils.extract import KafkaExtractor, Extractor
from utils.transform import DataTransformer, Transformer
from utils.load import ClickHouseLoader, Loader

from clickhouse_driver import Client
from confluent_kafka.cimpl import Consumer
from confluent_kafka.admin import AdminClient

from core.logger import LOGGER_CONFIG
from time import sleep

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


def etl(extrator: Extractor, transformer: Transformer, loader: Loader):
    logger.info("Start etl from Kafka to ClickHouse")
    events = extrator.get_batch_extractor(
        batch_size=int(kafka_settings.num_messages), timeout=int(kafka_settings.timeout)
    )
    transform_events = transformer.get_batch_transformer(events)
    loader.save_data(transform_events)


def main():
    logger.info("Start main")

    kafka_extractor = KafkaExtractor(
        consumer=Consumer(kafka_settings.get_kafka_config()),
        admin_client=AdminClient(kafka_settings.get_kafka_config()),
        topics=kafka_settings.get_topics(),
    )
    data_transformer = DataTransformer()
    click_house_loader = ClickHouseLoader(
        client=Client(
            host=clickhouse_settings.clickhouse_host,
            alt_hosts=clickhouse_settings.clickhouse_alt_hosts,
            password=clickhouse_settings.clickhouse_password,
        )
    )

    while True:
        try:
            etl(extrator=kafka_extractor, transformer=data_transformer, loader=click_house_loader)
        except Exception as ex:
            logger.error(f"Error etl data from Kafka to ClickHouse: {ex}")


if __name__ == "__main__":
    main()
