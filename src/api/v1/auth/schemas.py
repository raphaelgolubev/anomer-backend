from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr

from src.reusable.schemas import BaseSchema, Message # type: ignore


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


class SendEmailCode(BaseSchema):
    email: EmailStr


class VerifyEmail(BaseSchema):
    email: EmailStr
    code: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class ResetPasswordRequest(BaseSchema):
    email: EmailStr
    code: str
    new_password: str
   