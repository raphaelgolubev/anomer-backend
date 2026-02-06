""" Ошибки из Mongo """

from fastapi import Request, status
from fastapi.responses import JSONResponse

from pymongo.errors import DuplicateKeyError


async def handle_duplicate_in_document(request: Request, exc: DuplicateKeyError) -> JSONResponse:
    """
    Перехватывает ошибку дубликата БД в любом эндпойнте
    """
    endpoint = request.url.components.path
    # парсим исключение
    keys = exc.details["keyValue"].keys() if exc.details else ""
    # достаем поле документа, на которое ссылается ошибка
    key = list(keys)[0]
    # пустой словарь
    messages = {}

    # если ошибка в эндпойнте регистрации
    if "register" in endpoint:
        messages = {
            "name": "Пользователь с таким именем уже существует",
            "email": "Пользователь с таким адресом электронной почты уже существует",
        }
    # если название поля есть в словаре, то вернется сообщение из словаря
    # иначе дефолтное сообщение "Ошибка дубликата в поле"
    detail = messages.get(key, f"Ошибка дубликата в поле: {key}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": detail
        }
    )
