from beanie import Document, Indexed
from pydantic import EmailStr, ConfigDict


class User(Document):
    """ Модель пользователя в БД """

    name: Indexed(str, unique=True)
    """ юзернейм """

    email: Indexed(EmailStr, unique=True)
    """ почта """

    password: str
    """ хэшированный пароль"""

    class Settings:
        name = "users"
    
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "name": "Ivan",
                "email": "ivan@email.com",
                "password": "<some hash>"
            }
        }
    )
