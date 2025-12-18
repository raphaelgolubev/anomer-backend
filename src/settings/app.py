from pydantic_settings import BaseSettings

from src.settings.api import ApiV1Config
from src.settings.model_config import ModelConfig


class AppSettings(BaseSettings):
    """ Настройки приложения """

    name: str = "Anomer"
    """ Название приложения """

    version: str = "0.0.1"
    """ Версия приложения """

    prefix: str = "/api"
    """ Префикс пути """

    v1: ApiV1Config = ApiV1Config()
    """ Конфигурация первой версии API """

    model_config = ModelConfig(env_prefix="APP__")