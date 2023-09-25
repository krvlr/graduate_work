from pydantic import BaseSettings, Extra, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"
        extra = Extra.ignore


class LoggerSettings(BaseConfig):
    debug: str = Field(default="True", env="DEBUG")
    level: str = Field(default="INFO", env="LOGGING_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    default_handlers: list = ["console"]


class UserDataSettings(BaseConfig):
    host: str = Field(default="localhost", env="USER_DATA_REDIS_HOST")
    port: str = Field(default="6379", env="USER_DATA_REDIS_PORT")
    rating_pattern: str = Field(default="*:*:rating", env="")


class PersonalRecommendationsSettings(BaseConfig):
    host: str = Field(default="localhost", env="PERSONAL_RECOMMENDATIONS_HOST")
    port: str = Field(default="8000", env="PERSONAL_RECOMMENDATIONS_PORT")
    factors: str = Field(default="100", env="PERSONAL_RECOMMENDATIONS_FACTORS")
    regularization: str = Field(default="0.01", env="PERSONAL_RECOMMENDATIONS_REGULARIZATION")
    iterations: str = Field(default="20", env="PERSONAL_RECOMMENDATIONS_ITERATIONS")
    recommendation_count: str = Field(
        default="20", env="PERSONAL_RECOMMENDATIONS_RECOMMENDATION_COUNT"
    )
    personal_recommendations_path: str = Field(
        default="api/v1/personal_recommendations/personal",
        env="PERSONAL_RECOMMENDATIONS_PATH",
    )

    def get_url(self):
        return f"http://{self.host}:{self.port}/{self.personal_recommendations_path}"


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
    collection_user_recommendation: str = Field(
        default="user_recommendation", env="RECOMMENDATIONS_MONGODB_COLLECTION_USER_RECOMMENDATION"
    )

    def get_url(self):
        return f"mongodb://{self.host}:{self.port}"


logger_settings = LoggerSettings()
mongo_settings = MongoSettings()
personal_recommendations_settings = PersonalRecommendationsSettings()
user_data_settings = UserDataSettings()
