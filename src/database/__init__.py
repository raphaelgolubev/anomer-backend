from typing import Any
from pymongo import AsyncMongoClient

from src.settings import settings


mongo: AsyncMongoClient[dict[str, Any]] = AsyncMongoClient(
    host=settings.db.mongo_async_dsn,
)

database = mongo.get_database(settings.db.name)