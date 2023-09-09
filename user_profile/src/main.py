import logging.config

import uvicorn
from api.v1 import core, user_profile
from core.config import (
    jaeger_settings,
    base_settings,
    logger_settings,
)
from core.logger import LOGGER_CONFIG
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from utils.jaeger_config import configure_jaeger_tracer

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/user_profile/openapi",
    openapi_url="/api/user_profile/openapi.json",
    default_response_class=ORJSONResponse,
)


configure_jaeger_tracer(app, jaeger_settings.host, jaeger_settings.port)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


app.include_router(core.router, prefix="/api/v1/user_profile", tags=["core"])
app.include_router(user_profile.router, prefix="/api/v1/user_profile", tags=["user_profile"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGER_CONFIG,
        debug=logger_settings.debug,
    )
