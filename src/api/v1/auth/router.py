from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from beanie.operators import Or

from src.security.hashing_encoding import hash_password, verify_password
from src.database.models.user import User, UserStatus
import src.api.v1.auth.schemas as scheme


router = APIRouter()


@router.post("/register", response_model=scheme.NewCreatedUser)
async def register_new_user(user: scheme.CreateUser):
    """ Создание нового пользователя в базе данных """

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
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Аутентификация и авторизация пользователя """
    # ищем пользователя
    user = await User.find_one(
        Or(
            User.email == form_data.username,
            User.name == form_data.username
        )
    )
    # проверяем логин и пароль
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # проверяем статус        
    if user.status == UserStatus.created:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не подтвердили адрес электронной почты",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif user.status == UserStatus.banned:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Да ты забанен епта",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
    # если все ок, генерируем токен
        return {"status": "ok"}


@router.post("/reset_password")
async def reset_password():
    """ Восстановление пароля """
    pass