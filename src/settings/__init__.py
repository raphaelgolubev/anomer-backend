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


def test():
    app = settings.app.model_dump_json(indent=4)
    db = settings.db.model_dump_json(indent=4)
    mail = settings.mail.model_dump_json(indent=4)
    security = settings.security.model_dump_json(indent=4)
    redis = settings.redis.model_dump_json(indent=4)
    server = settings.server.model_dump_json(indent=4)
    
    print("=== App")
    print(app)

    print("=== Database")
    print(db)

    print("=== Mail")
    print(mail)

    print("=== Security")
    print(security)

    print("=== Redis")
    print(redis)

    print("=== Server")
    print(server)


settings = Settings()
