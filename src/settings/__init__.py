from src.settings.app import AppSettings
from src.settings.db import DatabaseSettings
from src.settings.mail import MailSettings
from src.settings.redis import RedisSettings
from src.settings.security import SecuritySettings
from src.settings.server import ServerSettings


class Settings:
    app = AppSettings()
    security = SecuritySettings()
    server = ServerSettings()
    db = DatabaseSettings()
    mail = MailSettings()
    redis = RedisSettings()


settings = Settings()
