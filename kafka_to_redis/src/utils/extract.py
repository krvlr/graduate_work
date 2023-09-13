import json
import logging

from abc import ABC, abstractmethod
from confluent_kafka.cimpl import Consumer
from confluent_kafka.admin import AdminClient, NewTopic
from utils.utils import backoff

logger = logging.getLogger(__name__)


class Extractor(ABC):
    @abstractmethod
    def get_batch_extractor(self, batch_size: int, timeout: int):
        pass


class KafkaExtractor(Extractor):
    def __init__(self, consumer: Consumer, admin_client: AdminClient, topics=list[str]):
        self.consumer = consumer
        self.admin_client = admin_client
        self.create_topics(topics=topics)
        self.consumer.subscribe(topics=topics)

    def create_topics(self, topics: list[str]):
        kafka_topics = self.admin_client.list_topics().topics
        new_topics = [
            NewTopic(topic, num_partitions=3, replication_factor=1)
            for topic in topics
            if topic not in kafka_topics
        ]
        if new_topics:
            fs = self.admin_client.create_topics(new_topics)

            for topic, f in fs.items():
                try:
                    f.result()  # The result itself is None
                    logger.info(f"Topic {topic} created")
                except Exception as ex:
                    logger.info(f"Failed to create topic {topic}: {ex}")

    @backoff()
    def get_batch_extractor(self, batch_size: int = 100, timeout: int = 5):
        events = self.consumer.consume(num_messages=batch_size, timeout=timeout)
        logger.info(f"Extract {len(events)} evens")

        for event in events:
            yield event.topic(), json.loads(event.value().decode("utf-8"))
