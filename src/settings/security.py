from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings

from src.settings.model_config import ModelConfig


class SecuritySettings(BaseSettings):
    """ Настройки безопасности """

    secret_pem_file: Path = Field(
        alias="SECURITY_PRIVATE_JWT", default=Path("certs/jwt-private.pem")
    )
    public_pem_file: Path = Field(
        alias="SECURITY_PUBLIC_JWT", default=Path("certs/jwt-public.pem")
    )
    algorithm: str = Field(default="RS256")
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 30 * 24 * 60  # 30 дней

    model_config = ModelConfig(env_prefix="SECURITY__")