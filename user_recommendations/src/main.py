import logging.config

import uvicorn
from api.v1 import core, user_recommendations
from core.config import (
    base_settings,
    jaeger_settings,
    logger_settings,
    mongo_settings,
    redis_settings,
)
from core.logger import LOGGER_CONFIG
from db import recommendation_provider, user_data_provider
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
from utils.jaeger_config import configure_jaeger_tracer

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/v1/recommendation/movies/openapi",
    openapi_url="/api/v1/recommendation/movies/openapi.json",
    default_response_class=ORJSONResponse,
)


configure_jaeger_tracer(app, jaeger_settings.host, jaeger_settings.port)


@app.on_event("startup")
async def startup():
    recommendation_provider.client = AsyncIOMotorClient(mongo_settings.get_url())
    user_data_provider.redis = Redis(host=redis_settings.redis_host, port=redis_settings.redis_port)


@app.on_event("shutdown")
async def shutdown():
    recommendation_provider.client.close()
    await user_data_provider.redis.close()


app.include_router(core.router, prefix="/api/v1/recommendation/movies", tags=["core"])
app.include_router(
    user_recommendations.router, prefix="/api/v1/recommendation/movies", tags=["recommendations"]
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGER_CONFIG,
        debug=logger_settings.debug,
    )
