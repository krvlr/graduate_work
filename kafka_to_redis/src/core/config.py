from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class KafkaSettings(BaseConfig):
    kafka_host: str = Field("127.0.0.1", env="KAFKA_HOST")
    kafka_port: str = Field(default="9092", env="KAFKA_PORT")
    num_messages: str = Field(default="200", env="KAFKA_EXTRACT_NUM_MESSAGES")
    timeout: str = Field(default="10", env="KAFKA_EXTRACT_TIMEOUT")
    group_id: str = Field(default="user_data", env="USER_DATA_KAFKA_GROUP_ID")
    auto_offset_reset: str = Field(default="smallest", env="KAFKA_AUTO_OFFSET_RESET")
    movies_topic: str = Field(default="movies_views", env="MOVIES_TOPIC")
    bookmarks_topic: str = Field(default="bookmarks", env="UGC_BOOKMARKS_TOPIC")
    ratings_topic: str = Field(default="ratings", env="UGC_RATINGS_TOPIC")
    reviews_topic: str = Field(default="reviews", env="UGC_REVIEWS_TOPIC")

    def get_topics(self):
        return [self.movies_topic, self.bookmarks_topic, self.ratings_topic, self.reviews_topic]

    def get_kafka_config(self) -> dict:
        return {
            "bootstrap.servers": f"{self.kafka_host}:{self.kafka_port}",
            "group.id": self.group_id,
            "auto.offset.reset": self.auto_offset_reset,
        }


class RedisSettings(BaseConfig):
    redis_host: str = Field(default="127.0.0.1", env="USER_DATA_REDIS_HOST")
    redis_port: str = Field(default="6379", env="USER_DATA_REDIS_PORT")


class LoggerSettings(BaseConfig):
    level: str = Field(default="INFO", env="LOGGING_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    default_handlers: list = ["console"]


base_settings = BaseSettings()
kafka_settings = KafkaSettings()
redis_settings = RedisSettings()
logger_settings = LoggerSettings()
