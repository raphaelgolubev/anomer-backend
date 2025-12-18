# interfaceingame.com
# CRT effect CSS / CRT scanline
# gameuidatabase.com

from src.settings import settings


def main():
    app = settings.app.model_dump()
    db = settings.db.model_dump()
    mail = settings.mail.model_dump()
    security = settings.security.model_dump()
    redis = settings.redis.model_dump()
    server = settings.server.model_dump()
    
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


if __name__ == "__main__":
    main()
