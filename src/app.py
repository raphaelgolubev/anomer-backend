from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse

from pymongo.errors import ConnectionFailure

from loguru import logger

from src.settings import settings
from src.database import mongo, database, create_beanie
from src.logger import setup_logging
from src.api import main_router
from src.utils.test_funcs import test_mongo, test_redis

async def startup():
    """Выполняется при запуске приложения"""

    setup_logging()

    try:
        # Пытаемся пингануть базу при старте
        await database.command('ping')
        logger.success("Successfully connected to MongoDB")
    except ConnectionFailure:
        logger.exception("MongoDB connection failed during startup")
    else:
        await create_beanie()
        logger.success("Beanie initialized")

        await test_mongo()
        await test_redis()


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
        await database.command('ping')
        return {"status": "ok", "db": "mongodb_connected"}
    except Exception as e:
        raise HTTPException(
            status_code=503, 
            detail=f"Database unavailable: {str(e)}"
        )