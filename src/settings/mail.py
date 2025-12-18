from pathlib import Path
from pydantic_settings import BaseSettings

from src.settings.model_config import ModelConfig


class MailSettings(BaseSettings):
    """
    Настройки подключения почтового сервера. (Gmail)
    """

    port: int = 465
    """ Порт почтового сервера """

    hostname: str | None = None
    """ Имя хоста почтового сервера """

    password: str | None = None
    """ Пароль пользователя """

    sender: str | None = None
    """ Отправитель. Например, `ivan.ivanov@gmail.com` """

    templates_path: Path | None = None
    """ Путь к HTML-шаблонам оформления исходящих писем """

    model_config = ModelConfig(env_prefix="MAIL__")
