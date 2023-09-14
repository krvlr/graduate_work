import json
import logging

from abc import ABC, abstractmethod
from utils.utils import backoff

from typing import Generator

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extensions import cursor as _cursor
from psycopg2.extras import DictCursor

logger = logging.getLogger(__name__)


@backoff()
def get_conn_postgresql(
    dbname: str,
    user: str,
    password: str,
    host: str,
    port: str,
    options: str = "",
    cursor_factory=DictCursor,
) -> _connection:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port,
        options=options,
        cursor_factory=cursor_factory,
    )
    return conn


class Extractor(ABC):
    @abstractmethod
    def get_batch_extractor(self, query: str):
        pass


class PostgresExtractor(Extractor):
    def __init__(self, conn: _connection, batch_size: int = 5000):
        self.conn = conn
        self.batch_size = batch_size

    def fetchmany_generator(self, cursor: _cursor) -> Generator:
        batch_iter = 0

        while True:
            batch = cursor.fetchmany(self.batch_size)

            if not batch:
                logger.info("Data loaded successfully!")
                break

            logger.info(f"Yield {batch_iter} batch")
            yield [dict(row) for row in batch]
            batch_iter += 1

    @backoff()
    def get_batch_extractor(self, query: str) -> Generator:
        cursor = self.conn.cursor()
        cursor.execute(query)
        data_generator = self.fetchmany_generator(cursor)
        return data_generator
