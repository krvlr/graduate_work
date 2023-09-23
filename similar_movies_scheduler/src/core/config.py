from pydantic import BaseSettings, Extra, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"
        extra = Extra.ignore


class BaseSettings(BaseConfig):
    elastic_batch_size: str = Field(
        default="500", env="SIMILAR_MOVIES_SCHEDULER_ELASTIC_BATCH_SIZE"
    )


class LoggerSettings(BaseConfig):
    debug: str = Field(default="True", env="DEBUG")
    level: str = Field(default="INFO", env="LOGGING_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    default_handlers: list = ["console"]


class SimilarMoviesSettings(BaseConfig):
    host: str = Field(default="localhost", env="SIMILAR_MOVIES_HOST")
    port: str = Field(default="8002", env="SIMILAR_MOVIES_PORT")
    radius: str = Field(default="0.2", env="SIMILAR_MOVIES_RADIUS")
    n_neighbors: str = Field(default="20", env="SIMILAR_MOVIES_N_NEIGHBOURS")
    metric: str = Field(default="cosine", env="SIMILAR_MOVIES_METRIC")
    similar_movies_nearest_neighbours_path: str = Field(
        default="api/v1/similar_movies/nearest_neighbours",
        env="SIMILAR_MOVIES_NEAREST_NEIGHBOURS_PATH",
    )

    def get_url(self):
        return f"http://{self.host}:{self.port}/{self.similar_movies_nearest_neighbours_path}"


class MoviesPreprocessorSettings(BaseConfig):
    host: str = Field(default="localhost", env="MOVIES_PREPROCESSOR_HOST")
    port: str = Field(default="8001", env="MOVIES_PREPROCESSOR_PORT")
    movies_preprocessor_vectorize_path: str = Field(
        default="api/v1/movies_preprocessor/vectorize", env="MOVIES_PREPROCESSOR_VECTORIZE_PATH"
    )

    def get_url(self):
        return f"http://{self.host}:{self.port}/{self.movies_preprocessor_vectorize_path}"


class ElasticSettings(BaseConfig):
    host: str = Field(default="localhost", env="ELASTIC_HOST")
    port: str = Field(default="9200", env="ELASTIC_PORT")

    def get_hosts(self):
        return [f"{self.host}:{self.port}"]


class MongoSettings(BaseConfig):
    host: str = Field(default="localhost", env="RECOMMENDATIONS_MONGODB_HOST")
    port: int = Field(default=27017, env="RECOMMENDATIONS_MONGODB_PORT")
    login: str = Field(
        default="default_general_recommendations", env="RECOMMENDATIONS_MONGODB_LOGIN"
    )
    password: str = Field(
        default="default_password", env="RECOMMENDATIONS_MONGODB_PASSWORD", repr=False
    )
    mongo_db_name: str = Field(default="recommendations", env="RECOMMENDATIONS_MONGODB_DB_NAME")
    collection_similar_movies: str = Field(
        default="similar_movies", env="RECOMMENDATIONS_MONGODB_COLLECTION_SIMILAR_MOVIES"
    )

    def get_url(self):
        return f"mongodb://{self.host}:{self.port}"


base_settings = BaseSettings()
logger_settings = LoggerSettings()
mongo_settings = MongoSettings()
elastic_settings = ElasticSettings()
movies_preprocessor_settings = MoviesPreprocessorSettings()
similar_movies_settings = SimilarMoviesSettings()
