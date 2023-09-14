import contextlib

import logging.config

from core.config import etl_settings, postgres_settings, redis_settings

from utils.extract import PostgresExtractor, Extractor, get_conn_postgresql
from utils.transform import DataTransformer, Transformer
from utils.load import Loader, RedisLoader

from core.logger import LOGGER_CONFIG

from utils.state import JsonFileStorage, State

from redis import Redis
from db.storage_provider import StorageRedisProvider

from datetime import datetime

from core.params import query_template

from time import sleep

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


def etl(extrator: Extractor, transformer: Transformer, loader: Loader, query: str):
    logger.info("Start etl from Postgres to Redis")
    batch_extractor = extrator.get_batch_extractor(query=query)
    batch_transformer = transformer.get_batch_transformer(batch_extractor=batch_extractor)
    loader.save_data(batch_transformer)


def main():
    logger.info("Start main")

    state = State(JsonFileStorage())

    data_transformer = DataTransformer()
    redis_loader = RedisLoader(
        storage=StorageRedisProvider(
            redis=Redis(host=redis_settings.redis_host, port=redis_settings.redis_port)
        )
    )

    while True:
        last_upload = state.get_state("last_upload", default=str(datetime.min))
        start_mark = str(datetime.now())

        try:
            with contextlib.closing(get_conn_postgresql(**postgres_settings.get_dsn())) as pg_conn:
                postgres_extractor = PostgresExtractor(
                    conn=pg_conn, batch_size=int(etl_settings.batch_size)
                )
                query = query_template.format(last_upload)

                etl(
                    extrator=postgres_extractor,
                    transformer=data_transformer,
                    loader=redis_loader,
                    query=query,
                )
                logger.info(
                    f"Upload modified beginning with {last_upload} data from Postgres to Redis complete successfully!"
                )
                state.set_state("last_upload", start_mark)

        except Exception as ex:
            logger.error(f"Error etl data from Postgres to Redis: {ex}")
            continue
        sleep(int(etl_settings.sleep_time))


if __name__ == "__main__":
    main()
