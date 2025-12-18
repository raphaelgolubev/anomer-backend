from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings

from src.settings.model_config import ModelConfig


class SecuritySettings(BaseSettings):
    """ Настройки безопасности """

    secret_pem_file: Path = Field(
        alias="SECURITY_PRIVATE_JWT", default=Path("certs/jwt-private.pem")
    )
    """ Путь к приватному ключу """

    public_pem_file: Path = Field(
        alias="SECURITY_PUBLIC_JWT", default=Path("certs/jwt-public.pem")
    )
    """ Путь к публичному ключу """

    algorithm: str = Field(default="RS256")
    """ Алгоритм шифрования """

    access_token_expire_minutes: int = 15
    """ В течение скольких минут истекает access_token """

    refresh_token_expire_minutes: int = 30 * 24 * 60  # 30 дней
    """ В течение скольких минут истекает refresh_token """

    model_config = ModelConfig(env_prefix="SECURITY__")