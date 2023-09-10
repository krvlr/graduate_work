from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class BaseSettings(BaseConfig):
    project_name: str = Field(default="user_profile", env="USER_PROFILE_PROJECT_NAME")
    secret_key: str = Field(default="SUPER-SECRET-KEY", repr=False, env="JWT_SECRET_KEY")


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
    port: int = Field(default=6831, env="JAEGER_PORT")


class PostgresSettings(BaseConfig):
    db_host: str = Field(default="127.0.0.1", env="USER_PROFILE_DB_HOST")
    db_port: str = Field(default="5432", env="USER_PROFILE_DB_PORT")
    db_name: str = Field(default="user_profile_database", env="USER_PROFILE_DB_NAME")
    db_user: str = Field(default="admin", env="USER_PROFILE_DB_USER")
    db_password: str = Field(default="admin", env="USER_PROFILE_DB_PASSWORD")

    def get_db_uri(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    def get_db_uri_alembic(self) -> str:
        print(self.db_host, self.db_port, self.db_name, self.db_user, self.db_password)
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


base_settings = BaseSettings()
logger_settings = LoggerSettings()
jaeger_settings = JaegerSettings()
postgres_settings = PostgresSettings()
