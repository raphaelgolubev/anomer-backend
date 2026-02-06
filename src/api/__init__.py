from fastapi import APIRouter

from src.settings import settings
from src.api.v1.auth.router import router as auth_router
from src.api.v1.users.router import router as users_router


main_router = APIRouter()
main_router.include_router(
    auth_router,
    prefix=settings.app.v1.auth,
    tags=["Вход и регистрация"]
)
main_router.include_router(
    users_router,
    prefix=settings.app.v1.users,
    tags=["Пользователи"]
)