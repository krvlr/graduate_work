from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class BaseSettings(BaseConfig):
    project_name: str = Field(default="preprocessor", env="MOVIES_PREPROCESSOR_PROJECT_NAME")
    stopwords_path: str = "stopwords/"
    pickle_path: str = "pickle/"
    weights_name: str = "idf_weights"
    phrases_path: str = "pickle/phrases"
    wv_path: str = "pickle/w2v.wordvectors"
    stopwords_filenames: list[str] = ["english"]


class JaegerSettings(BaseConfig):
    enable_tracer: bool = Field(default=True, env="ENABLE_TRACER")
    host: str = Field(default="127.0.0.1", env="JAEGER_HOST")
    port: int = Field(default=6831, env="JAEGER_PORT")


class LoggerSettings(BaseConfig):
    debug: str = Field(default="True", env="DEBUG")
    level: str = Field(default="INFO", env="LOGGING_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    default_handlers: list = ["console"]


base_settings = BaseSettings()
jaeger_settings = JaegerSettings()
logger_settings = LoggerSettings()
