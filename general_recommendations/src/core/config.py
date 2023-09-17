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


class GeneralDataMongodbSettings(BaseConfig):
    host: str = Field(default="mongo", env="GENERAL_DATA_MONGODB_HOST")
    port: int = Field(default=27017, env="GENERAL_DATA_MONGODB_PORT")
    login: str = Field(default="default_general_recommendations", env="GENERAL_DATA_MONGODB_LOGIN")
    password: str = Field(
        default="default_password", env="GENERAL_DATA_MONGODB_PASSWORD", repr=False
    )
    mongo_db_name: str = Field(
        default="general_recommendations", env="GENERAL_DATA_MONGODB_DB_NAME"
    )
    collection_movies: str = Field(default="movies", env="GENERAL_DATA_MONGODB_COLLECTION")


base_settings = BaseSettings()
logger_settings = LoggerSettings()
jaeger_settings = JaegerSettings()
general_data_mongodb_settings = GeneralDataMongodbSettings()
