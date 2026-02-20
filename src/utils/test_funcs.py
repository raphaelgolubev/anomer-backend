from loguru import logger

from src.settings import settings
from src.database import database
from src.database.models import User
from src.utils.redis_client import redis_client


def test_settings():
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


async def test_mongo():
    users: list[User] = []
    for i in range(3):
        name = f"test_user_{i+1}"
        usr = User(
            name=name,
            email=f"test_{i+1}@test.com",
            password="<hash>"
        )
        users.append(usr)
        logger.debug(f"added user {name}")
    
    result = await User.insert_many(users)

    logger.success(f"Документы добавлены базу данных {database.name}")
    logger.debug("Идентификаторы документов: ")
    for id in result.inserted_ids:
        logger.debug(f"\tDocument {id}")

    deleted = await User.find({"_id": {"$in": result.inserted_ids}}).delete()
    if deleted:
        logger.success(f"Все созданные документы удалены: {deleted.deleted_count} записей")
    else:
        logger.error(f"Не удалось удалить документы")


async def test_redis():
    is_available: bool = await redis_client.redis.ping() # type: ignore
    if is_available:
        logger.success("Redis is connected")
    else:
        logger.error("Redis unavailable")