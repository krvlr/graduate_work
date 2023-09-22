import asyncio
import logging.config

from core.logger import LOGGER_CONFIG
from services.recommendation_service import get_recommendation_service

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


async def main():
    recommendation_service = get_recommendation_service()
    await recommendation_service.create_recommendations()


if __name__ == "__main__":
    asyncio.run(main())
