from beanie import PydanticObjectId
from pydantic import EmailStr

from src.reusable.base_schema import BaseSchema


class CreateUser(BaseSchema):
    """ Форма для создания юзера """
    name: str
    email: EmailStr
    password: str


class NewCreatedUser(BaseSchema):
    """ Форма ответа от сервера """
    id: PydanticObjectId
    name: str
    email: EmailStr

   