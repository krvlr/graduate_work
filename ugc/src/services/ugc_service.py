from typing import Annotated

from db.base_db import QueueProvider
from db.kafka_provider import get_kafka_provider
from fastapi import Depends


class UGCService:
    def __init__(self, queue_provider: QueueProvider):
        self.queue_provider = queue_provider

    async def register_event(self, topic: str, event: dict, key: str):
        await self.queue_provider.send(topic=topic, event=event, key=key)


def get_ugc_service(
    queue_provider: Annotated[QueueProvider, Depends(get_kafka_provider)]
) -> UGCService:
    return UGCService(queue_provider=queue_provider)
