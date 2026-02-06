from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse

from pymongo.errors import ConnectionFailure
from redis.exceptions import ConnectionError

from loguru import logger

from src.settings import settings
from src.database import mongo, database, create_beanie
from src.logger import setup_logging
from src.api import main_router
from src.utils.redis_client import redis_client
from src.exceptions import register_exception_handlers


async def startup():
    """Выполняется при запуске приложения"""

    setup_logging()

    # Пытаемся пингануть монгу и редис при старте
    try:
        await database.command('ping')
        logger.success("Успешно подключился к MongoDB")

        await redis_client.redis.ping() # type: ignore
        logger.success("Успешно подключился к Redis")

    except ConnectionFailure as e:
        logger.critical(f"Не удалось соединиться с MongoDB: {e}")
        raise RuntimeError("База лежит!!!")

    except ConnectionError as e:
        logger.critical(f"Не удалось соединиться с Redis: {e}")
        raise RuntimeError("Редис лежит!!!")

    else:
        await create_beanie()
        logger.success("Beanie инициализирован")


async def shutdown():
    """Выполняется при остановке приложения"""
    logger.debug("Закрываем соединеие с базой данных...")
    await mongo.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл приложения"""
    try:
        await startup()
        yield
    finally:
        # Сработает и при штатном выходе, и если startup упал на полпути
        await shutdown()


# создаем инстанс приложения
app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    version=settings.app.version,
    description="Anomer backend monolith",
)

# включаем роутеры
app.include_router(main_router)

# регистрируем обработчики ошибок
register_exception_handlers(app)


@app.get("/health")
async def health_check():
    """Эндпоинт для мониторинга"""
    try:
        await database.command('ping')
        return {"status": "ok", "db": "mongodb_connected"}
    except Exception as e:
        raise HTTPException(
            status_code=503, 
            detail=f"База данных недоступна: {str(e)}"
        )