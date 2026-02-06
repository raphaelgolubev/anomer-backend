from fastapi import FastAPI
from src.exceptions import mongo_errors


def register_exception_handlers(app: FastAPI):
    """
    Регистрирует все обработчики исключений в FastAPI приложении.

    Args:
        app: FastAPI приложение
    """

    # Регистрируем обработчики
    app.add_exception_handler(
        mongo_errors.DuplicateKeyError, 
        mongo_errors.handle_duplicate_in_document # type: ignore
    )