import logging.config
import os
from pathlib import Path

import uvicorn
from api.v1 import core, document
from core.config import base_settings, jaeger_settings, logger_settings
from core.logger import LOGGER_CONFIG
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from gensim.models import KeyedVectors
from gensim.models.phrases import Phrases
from utils import preprocessor, vectorizer
from utils.jaeger_config import configure_jaeger_tracer
from utils.utils import load_pickle

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/v1/movies_preprocessor/openapi",
    openapi_url="/api/v1/movies_preprocessor/openapi.json",
    default_response_class=ORJSONResponse,
)


configure_jaeger_tracer(app, jaeger_settings.host, jaeger_settings.port)


@app.on_event("startup")
async def startup():
    logger.info(os.path.join(Path.cwd(), base_settings.phrases_path))
    preprocessor.phrases = Phrases.load(os.path.join(Path.cwd(), base_settings.phrases_path))
    vectorizer.wv = KeyedVectors.load(os.path.join(Path.cwd(), base_settings.wv_path), mmap="r")
    vectorizer.weights = load_pickle(
        path_dir=Path.joinpath(Path.cwd(), base_settings.pickle_path),
        filename=base_settings.weights_name,
    )


@app.on_event("shutdown")
async def shutdown():
    pass


app.include_router(
    document.router, prefix="/api/v1/movies_preprocessor", tags=["movies_preprocessor"]
)
app.include_router(core.router, prefix="/api/v1/movies_preprocessor", tags=["core"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGER_CONFIG,
        debug=logger_settings.debug,
    )
