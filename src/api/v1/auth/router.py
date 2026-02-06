from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm

from beanie.operators import Or, Set

from src.security.hashing_encoding import hash_password, verify_password
from src.security.tokens import create_token, TokenType
from src.utils.emails import send_verification_code
from src.database.models.user import User, UserStatus
import src.api.v1.auth.schemas as scheme
import src.api.v1.auth.service as service


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


@router.post("/send_email_code", response_model=scheme.EmailSent)
async def send_email_code(input: scheme.SendEmailCode, background_tasks: BackgroundTasks):
    """ Отправляет одноразовый код на электронную почту """
    # ищем пользователя в базе
    user = await User.find_one(User.email == input.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с такой почтой не найден"
        )

    if user.status == UserStatus.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы уже подтвердили адрес электронной почты"
        )

    # генерируем код
    code = service.generate_verification_code()
    # сохраняем его в redis
    is_saved = await service.save_otp_in_redis(
        email=input.email,
        code=code
    )

    if is_saved:
        # отправляем письмо в бэкграунде
        background_tasks.add_task(
            send_verification_code,
            to_email=input.email,
            code=code
        )

        return scheme.EmailSent(message="Письмо отправлено")
    
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Не удалось отправить письмо"
    )


@router.post("/verify_email", response_model=scheme.EmailVerified)
async def verify_email(input: scheme.VerifyEmail):
    user = await User.find_one(User.email == input.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким адресом не найден"
        )

    is_correct = await service.verify_email_code(
        email=input.email, 
        code=input.code
    )

    if user.status == UserStatus.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Почта уже подтверждена"
        )

    if is_correct:
        await user.update(Set({User.status: UserStatus.active})) 

        await service.remove_code(email=input.email)

        return scheme.EmailVerified(
            message="Вы успешно подтвердили адрес электронной почты"
        )
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Код подтверждения неверный"
    )


@router.post("/login", response_model=scheme.TokenInfo)
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
    if user.status == UserStatus.banned:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Да ты забанен епта",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # если все ок, генерируем токены
    access_token = create_token(user.name, user.role.value, TokenType.ACCESS_TOKEN_TYPE)
    refresh_token = create_token(user.name, user.role.value, TokenType.REFRESH_TOKEN_TYPE)
    
    return scheme.TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/reset_password")
async def reset_password():
    """ Восстановление пароля """
    pass