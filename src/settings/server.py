from pydantic_settings import BaseSettings

from src.settings.model_config import ModelConfig


class ServerSettings(BaseSettings):
    """ Настройки сервера """

    host: str | None = None
    """ Имя хоста """

    port: int | None = None
    """ Порт сервера """

    model_config = ModelConfig(env_prefix="SERVER__")
