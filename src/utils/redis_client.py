from typing import Any
import redis.asyncio as redis

from src.settings import settings


class RedisClient:
    """Клиент для работы с Redis"""

    def __init__(self):
        redis_kwargs: dict[str, Any] = {
            "host": settings.redis.host,
            "port": settings.redis.port,
            "db": settings.redis.db,
            "decode_responses": True,
        }

        # Добавляем password если указан
        if settings.redis.password:
            redis_kwargs["password"] = settings.redis.password

        self.redis = redis.Redis(**redis_kwargs)


redis_client = RedisClient()