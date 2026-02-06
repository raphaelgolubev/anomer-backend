from enum import Enum

from beanie import Document, Indexed
from pydantic import EmailStr, ConfigDict


class UserStatus(str, Enum):
    """ Статус пользователя """

    created = "CREATED"
    """ Создан - он только что создан и требуется подтвердить почту """

    active = "ACTIVE"
    """ Активен - юзер подтвердил почту. Он может пользоваться приложением """

    banned = "BANNED"
    """ Пользователь забанен """


class UserRole(str, Enum):
    """ Роль пользователя """

    default = "DEFAULT"
    """ Самый обычный юзер """

    super_user = "SUPER_USER"
    """ Юзер с расширенными возможностями """


class User(Document):
    """ Модель пользователя в БД """

    name: Indexed(str, unique=True)
    """ юзернейм """

    email: Indexed(EmailStr, unique=True)
    """ почта """

    password: str
    """ хэшированный пароль"""

    status: UserStatus = UserStatus.created
    """ статус пользователя, по умолчанию 'CREATED' """

    role: UserRole = UserRole.default
    """ роль пользователя, по умолчанию 'DEFAULT' """

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
