import uvicorn
from api.v1 import core, films, genres, persons
from core.config import (
    base_settings,
    elastic_settings,
    jaeger_settings,
    logger_settings,
    redis_settings,
)
from core.logger import LOGGER_CONFIG
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from utils.jaeger_config import configure_jaeger_tracer

app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/movies/openapi",
    openapi_url="/api/movies/openapi.json",
    default_response_class=ORJSONResponse,
)

configure_jaeger_tracer(app, jaeger_settings.host, jaeger_settings.port)


@app.on_event("startup")
async def startup():
    redis.redis = Redis(host=redis_settings.host, port=redis_settings.port)
    elastic.es = AsyncElasticsearch(hosts=[f"{elastic_settings.host}:{elastic_settings.port}"])


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix="/api/v1/movies/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/movies/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/movies/persons", tags=["persons"])
app.include_router(core.router, prefix="/api/v1/movies", tags=["core"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGER_CONFIG,
        debug=logger_settings.debug,
    )
