from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse

from pymongo.errors import ConnectionFailure
from beanie.operators import In

from loguru import logger

from src.settings import settings
from src.database import mongo, database, create_beanie
from src.logger import setup_logging

from src.api import main_router

async def startup():
    """Выполняется при запуске приложения"""

    setup_logging()

    try:
        # Пытаемся пингануть базу при старте
        await database.command('ping')
        logger.success("✅ Successfully connected to MongoDB")
    except ConnectionFailure:
        logger.exception("❌ MongoDB connection failed during startup")
    else:
        await create_beanie()
        logger.success("✅ Beanie initialized")

        async def test_db():
            from src.database.models import User

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
            
        await test_db()


async def shutdown():
    """Выполняется при остановке приложения"""
    logger.debug("Закрываем соединеие с базой данных...")
    await mongo.close()
    logger.debug("Приложение остановлено")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл приложения"""
    await startup()
    yield
    await shutdown()


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    version=settings.app.version,
    description="Anomer backend monolith",
)

app.include_router(main_router)

@app.get("/health")
async def health_check():
    """Эндпоинт для мониторинга"""
    try:
        # Асинхронный ping — самый легкий способ проверки
        await database.command('ping')
        return {"status": "ok", "db": "mongodb_connected"}
    except Exception as e:
        # Возвращаем 503, если БД недоступна
        raise HTTPException(
            status_code=503, 
            detail=f"Database unavailable: {str(e)}"
        )