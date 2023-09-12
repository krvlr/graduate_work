import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from api.v1 import core, general_recommendations
from core.config import (
    jaeger_settings,
    base_settings,
    mongodb_settings,
)
from core.logger import LOGGER_CONFIG
from db import mongodb
from utils.jaeger_config import configure_jaeger_tracer

app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/general_recommendations/openapi",
    openapi_url="/api/general_recommendations/openapi.json",
    default_response_class=ORJSONResponse,
)

configure_jaeger_tracer(app, jaeger_settings.host, jaeger_settings.port)


@app.on_event("startup")
async def startup():
    mongodb.client = AsyncIOMotorClient(
        f"mongodb://{mongodb_settings.login}:{mongodb_settings.password}@"
        f"{mongodb_settings.mongodb_host}:{mongodb_settings.mongodb_port}/"
        f"?authSource={mongodb_settings.mongo_db_name}&authMechanism=SCRAM-SHA-256"
    )


@app.on_event("shutdown")
async def shutdown():
    await mongodb.client.close()


app.include_router(core.router, prefix="/api/v1/general_recommendations", tags=["core"])
app.include_router(
    general_recommendations.router,
    prefix="/api/v1/general_recommendations",
    tags=["general_recommendations"],
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGER_CONFIG,
    )
