from pydantic_settings import BaseSettings

from src.settings.model_config import ModelConfig


class DatabaseSettings(BaseSettings):
    """
    Настройки подключения к СУБД.
    """

    user: str | None = None
    """ От какого имени пользователя обращаться в СУБД """

    password: str | None = None
    """ Пароль пользователя СУБД """

    name: str | None = None
    """ Наименование базы данных в СУБД """

    port: int | None = None
    """ Порт сервера СУБД """

    host: str | None = None
    """ Имя хоста сервера СУБД """

    @property
    def async_dsn(self):
        """
        Строка подключения к PostgreSQL с использованием AsyncPG.
        """
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    # env ignore
    naming_conventions: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    model_config = ModelConfig(env_prefix="DB__")