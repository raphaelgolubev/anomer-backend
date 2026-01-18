from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.settings import settings


async def startup():
    """Выполняется при запуске приложения"""
    pass


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