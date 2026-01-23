from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse

from pymongo.errors import ConnectionFailure

from src.settings import settings
from src.database import database, create_beanie


async def startup():
    """Выполняется при запуске приложения"""
    try:
        # Пытаемся пингануть базу при старте
        await database.command('ping')
        print("✅ Successfully connected to MongoDB")
    except ConnectionFailure:
        print("❌ MongoDB connection failed during startup")
    else:
        await create_beanie()
        print("✅ Beanie initialized")


async def shutdown():
    """Выполняется при остановке приложения"""
    pass


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