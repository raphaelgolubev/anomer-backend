from beanie import Document
from pydantic import EmailStr, ConfigDict


class User(Document):
    """ Модель пользователя """

    name: str
    """ юзернейм """

    email: EmailStr
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
