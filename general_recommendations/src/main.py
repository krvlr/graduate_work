import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from api.v1 import core, general_recommendations, rating
from core.config import (
    jaeger_settings,
    base_settings,
    general_data_mongodb_settings,
)
from core.logger import LOGGER_CONFIG
from db import mongodb
from utils.jaeger_config import configure_jaeger_tracer

app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/v1/general_recommendations/movies/openapi",
    openapi_url="/api/v1/general_recommendations/movies/openapi.json",
    default_response_class=ORJSONResponse,
)

configure_jaeger_tracer(app, jaeger_settings.host, jaeger_settings.port)


@app.on_event("startup")
async def startup():
    mongodb.recommendations_client = AsyncIOMotorClient(
        f"mongodb://{general_data_mongodb_settings.login}:{general_data_mongodb_settings.password}@"
        f"{general_data_mongodb_settings.host}:{general_data_mongodb_settings.port}/"
        f"?authSource={general_data_mongodb_settings.mongo_db_name}&authMechanism=SCRAM-SHA-256"
    )


@app.on_event("shutdown")
async def shutdown():
    await mongodb.recommendations_client.close()


app.include_router(core.router, prefix="/api/v1", tags=["core"])
app.include_router(
    general_recommendations.router,
    prefix="/api/v1/general_recommendations/movies",
    tags=["general_recommendations"],
)
app.include_router(
    rating.router,
    prefix="/api/v1/general_recommendations/movies",
    tags=["ratings"],
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGER_CONFIG,
    )
