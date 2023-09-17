import uvicorn
from aiokafka import AIOKafkaProducer
from api.v1 import core, ugc
from core.config import base_settings, jaeger_settings, kafka_settings, logger_settings
from core.logger import LOGGER_CONFIG
from db import kafka_provider
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from utils.jaeger_config import configure_jaeger_tracer

app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/v1/ugc/openapi",
    openapi_url="/api/v1/ugc/openapi.json",
    default_response_class=ORJSONResponse,
)


configure_jaeger_tracer(app, jaeger_settings.host, jaeger_settings.port)


@app.on_event("startup")
async def startup():
    kafka_provider.kafka_producer = AIOKafkaProducer(
        bootstrap_servers=[f"{kafka_settings.host}:{kafka_settings.port}"]
    )
    await kafka_provider.kafka_producer.start()


@app.on_event("shutdown")
async def shutdown():
    await kafka_provider.kafka_producer.stop()


app.include_router(ugc.router, prefix="/api/v1/ugc", tags=["ugc"])
app.include_router(core.router, prefix="/api/v1/ugc", tags=["core"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGER_CONFIG,
        debug=logger_settings.debug,
    )
