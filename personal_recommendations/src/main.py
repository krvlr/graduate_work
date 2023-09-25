import logging.config
import os

import uvicorn
from api.v1 import core, personal_recommendations
from core.config import base_settings, jaeger_settings, logger_settings
from core.logger import LOGGER_CONFIG
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from utils.jaeger_config import configure_jaeger_tracer

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/v1/personal_recommendations/openapi",
    openapi_url="/api/v1/personal_recommendations/openapi.json",
    default_response_class=ORJSONResponse,
)


configure_jaeger_tracer(app, jaeger_settings.host, jaeger_settings.port)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


app.include_router(
    personal_recommendations.router,
    prefix="/api/v1/personal_recommendations",
    tags=["personal_recommendations"],
)
app.include_router(core.router, prefix="/api/v1/personal_recommendations", tags=["core"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGER_CONFIG,
        debug=logger_settings.debug,
    )
