from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError

from src.security.hashing_encoding import hash_password
from src.database.models.user import User
import src.api.v1.auth.schemas as scheme


router = APIRouter()


@router.post("/register")
async def register_new_user(user: scheme.UserCreate) -> scheme.CreatedUser:
    """ Регистрация нового пользователя """

    hashed = hash_password(user.password).decode()

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed
    )

    try:
        inserted_user = await new_user.insert()
        return inserted_user
    except DuplicateKeyError as e:
        key = list(e.details["keyValue"].keys())[0]

        if key == "name":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким именем уже существует"
            )
        elif key == "email":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Дупликат"
            )


@router.post("/login")
async def login_user():
    """ Аутентификация и авторизация пользователя """
    pass


@router.post("/reset_password")
async def reset_password():
    """ Восстановление пароля """
    pass