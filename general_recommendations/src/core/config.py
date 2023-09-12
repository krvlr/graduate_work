from pydantic import Field
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class BaseSettings(BaseConfig):
    project_name: str = Field(default="general_recommendations", env="PROJECT_NAME")


class LoggerSettings(BaseConfig):
    debug: str = Field(default="True", env="DEBUG")
    level: str = Field(default="INFO", env="LOGGING_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    default_handlers: list = ["console"]


class JaegerSettings(BaseConfig):
    enable_tracer: bool = Field(default=True, env="ENABLE_TRACER")
    host: str = Field(default="jaeger", env="JAEGER_HOST")
    port: int = Field(default=6831, env="JAEGER_PORT")


class MongodbSettings(BaseConfig):
    mongodb_host: str = Field(default="mongos1", env="GENERAL_DATA_MONGODB_HOST")
    mongodb_port: int = Field(default=27017, env="GENERAL_DATA_MONGODB_PORT")
    login: str = Field(default="default", env="GENERAL_DATA_MONGODB_LOGIN")
    password: str = Field(default="default_password", env="GENERAL_DATA_MONGODB_PASSWORD")
    mongo_db_name: str = Field(default="general_data", env="GENERAL_DATA_MONGODB_DB_NAME")


base_settings = BaseSettings()
logger_settings = LoggerSettings()
jaeger_settings = JaegerSettings()
mongodb_settings = MongodbSettings()
