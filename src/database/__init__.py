from typing import Any
from pymongo import AsyncMongoClient
from beanie import init_beanie # type: ignore

from src.settings import settings
from src.database.models import document_models


mongo: AsyncMongoClient[dict[str, Any]] = AsyncMongoClient(
    host=settings.db.mongo_async_dsn,
)

database = mongo.get_database(settings.db.name)


async def create_beanie():
    await init_beanie(
        database=database,
        document_models=document_models
    )
