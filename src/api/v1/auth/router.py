from fastapi import APIRouter

from src.security.hashing_encoding import hash_password
from src.database.models.user import User
import src.api.v1.auth.schemas as scheme


router = APIRouter()


@router.post("/register", response_model=scheme.NewCreatedUser)
async def register_new_user(user: scheme.CreateUser):
    """ Регистрация нового пользователя """

    # хэшируем пароль
    hashed = hash_password(user.password).decode()
    # создаем юзера
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed
    )

    inserted_user = await new_user.insert()
    return inserted_user


@router.post("/login")
async def login_user():
    """ Аутентификация и авторизация пользователя """
    pass


@router.post("/reset_password")
async def reset_password():
    """ Восстановление пароля """
    pass