from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class ETLSettings(BaseConfig):
    sleep_time: str = Field(default="60", env="POSTGRES_TO_REDIS_SLEEP_TIME")
    batch_size: str = Field(default="500", env="POSTGRES_TO_REDIS_BATCH_SIZE")


class PostgresSettings(BaseConfig):
    db_host: str = Field(default="127.0.0.1", env="USER_PROFILE_DB_HOST")
    db_port: str = Field(default="5432", env="USER_PROFILE_DB_PORT")
    db_name: str = Field(default="user_profile_database", env="USER_PROFILE_DB_NAME")
    db_user: str = Field(default="admin", env="USER_PROFILE_DB_USER")
    db_password: str = Field(default="admin", env="USER_PROFILE_DB_PASSWORD")

    def get_dsn(self):
        return {
            "host": self.db_host,
            "port": self.db_port,
            "dbname": self.db_name,
            "user": self.db_user,
            "password": self.db_password,
        }


class RedisSettings(BaseConfig):
    redis_host: str = Field(default="127.0.0.1", env="USER_DATA_REDIS_HOST")
    redis_port: str = Field(default="6379", env="USER_DATA_REDIS_PORT")
    user_profile_key: str = Field(default="user_profile", env="USER_DATA_USER_PROFILE_KEY")


class LoggerSettings(BaseConfig):
    level: str = Field(default="INFO", env="LOGGING_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    default_handlers: list = ["console"]


etl_settings = ETLSettings()
redis_settings = RedisSettings()
postgres_settings = PostgresSettings()
logger_settings = LoggerSettings()
