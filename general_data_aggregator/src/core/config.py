from pydantic import Field
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class LoggerSettings(BaseConfig):
    debug: str = Field(default="True", env="DEBUG")
    level: str = Field(default="INFO", env="LOGGING_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    default_handlers: list = ["console"]


class SourcesMongodbSettings(BaseConfig):
    mongodb_host: str = Field(default="mongos1", env="MONGODB_HOST")
    mongodb_port: int = Field(default=27017, env="MONGODB_PORT")
    login: str = Field(default="default", env="MONGODB_LOGIN")
    password: str = Field(default="default_password", env="MONGODB_PASSWORD")
    mongo_db_name: str = Field(default="ugc2", env="MONGODB_DB_NAME")
    collection_bookmark: str = Field(default="bookmark", env="MONGODB_COLLECTION_BOOKMARK")
    collection_review: str = Field(default="review", env="MONGODB_COLLECTION_REVIEW")
    collection_rating: str = Field(default="rating", env="MONGODB_COLLECTION_RATING")


class SourcesElasticSettings(BaseConfig):
    host: str = Field(default="elasticsearch-movies", env="ELASTIC_HOST")
    port: int = Field(default=9200, env="ELASTIC_PORT")


class GeneralDataMongodbSettings(BaseConfig):
    mongodb_host: str = Field(default="mongos1", env="GENERAL_DATA_MONGODB_HOST")
    mongodb_port: int = Field(default=27017, env="GENERAL_DATA_MONGODB_PORT")
    login: str = Field(default="default", env="GENERAL_DATA_MONGODB_LOGIN")
    password: str = Field(default="default_password", env="GENERAL_DATA_MONGODB_PASSWORD")
    mongo_db_name: str = Field(default="general_data", env="GENERAL_DATA_MONGODB_DB_NAME")


logger_settings = LoggerSettings()
sources_mongodb_settings = SourcesMongodbSettings()
sources_elastic_settings = SourcesElasticSettings()
general_data_mongodb_settings = GeneralDataMongodbSettings()
