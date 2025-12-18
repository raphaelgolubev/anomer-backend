from pydantic_settings import BaseSettings

from src.settings.model_config import ModelConfig


class RedisSettings(BaseSettings):
    """ Настройки подключения к Redis """

    host: str = "localhost"
    """ Хост для подключения к серверу `Redis` """

    port: int = 6379
    """ Порт для подключения к серверу `Redis` """

    db: int = 0
    """ Название базы данных """

    password: str | None = None
    """ Пароль для аутентификации """

    verification_code_ttl: int = 300  # 5 минут в секундах
    """ Срок жизни верификационного кода в секундах """

    model_config = ModelConfig(env_prefix="REDIS__")