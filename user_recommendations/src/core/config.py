from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class BaseSettings(BaseConfig):
    project_name: str = Field(default="user_recommendation", env="USER_RECOMMENDATION_PROJECT_NAME")
    secret_key: str = Field(default="SUPER-SECRET-KEY", repr=False, env="JWT_SECRET_KEY")
    user_recommendation_size: int = Field(default=10, env="USER_RECOMMENDATION_SIZE", ge=1)


class LoggerSettings(BaseConfig):
    debug: str = Field(default="True", env="DEBUG")
    level: str = Field(default="INFO", env="LOGGING_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    default_handlers: list = ["console"]


class JaegerSettings(BaseConfig):
    enable_tracer: bool = Field(default=True, env="ENABLE_TRACER")
    host: str = Field(default="127.0.0.1", env="JAEGER_HOST")
    port: str = Field(default="6831", env="JAEGER_PORT")


class MongoSettings(BaseConfig):
    mongodb_host: str = Field(default="localhost", env="MONGODB_HOST")
    mongodb_port: str = Field(default="27017", env="MONGODB_PORT")
    login: str = Field(default="default", env="MONGODB_LOGIN")
    password: str = Field(default="default_password", env="MONGODB_PASSWORD")
    mongo_db_name: str = Field(default="ugc", env="MONGODB_DB_NAME")
    collection_similar_movies: str = Field(
        default="similar_movies", env="MONGODB_COLLECTION_SIMILAR_MOVIES"
    )
    collection_user_recommendation: str = Field(
        default="user_recommendation", env="MONGODB_COLLECTION_USER_RECOMMENDATION"
    )

    def get_url(self):
        return f"mongodb://{self.mongodb_host}:{self.mongodb_port}"


class MovieSettings(BaseConfig):
    host: str = Field(default="localhost", env="MOVIES_API_HOST")
    port: str = Field(default="8002", env="MOVIES_API_PORT")
    movie_detail_path: str = Field(default="api/v1/movies/films")

    def get_url(self):
        return f"http://{self.host}:{self.port}/{self.movie_detail_path}"


class RedisSettings(BaseConfig):
    redis_host: str = Field(default="127.0.0.1", env="USER_DATA_REDIS_HOST")
    redis_port: str = Field(default="6379", env="USER_DATA_REDIS_PORT")
    user_profile_key: str = Field(default="user_profile", env="USER_DATA_USER_PROFILE_KEY")


class GeneralRecommendationsSettings(BaseConfig):
    host: str = Field(default="localhost", env="GENERAL_RECOMMENDATIONS_API_HOST")
    port: str = Field(default="8003", env="GENERAL_RECOMMENDATIONS_API_PORT")
    replacement_path: str = Field(default="api/v1/general_recommendations/movies/replacement")
    ratings_path: str = Field(default="api/v1/general_recommendations/movies/ratings")

    def get_replacement_url(self):
        return f"http://{self.host}:{self.port}/{self.replacement_path}"

    def get_rating_url(self):
        return f"http://{self.host}:{self.port}/{self.ratings_path}"


base_settings = BaseSettings()
logger_settings = LoggerSettings()
jaeger_settings = JaegerSettings()
mongo_settings = MongoSettings()
movie_settings = MovieSettings()
redis_settings = RedisSettings()
general_recommendations_settings = GeneralRecommendationsSettings()
