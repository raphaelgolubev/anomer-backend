from beanie import PydanticObjectId
from pydantic import ConfigDict, Field, BaseModel, EmailStr


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        # Позволяет мапить данные из объектов Beanie (ORM/ODM mode)
        from_attributes=True,
        # Позволяет создавать модель, используя как 'id', так и '_id'
        populate_by_name=True 
    )


class UserCreate(BaseSchema):
    name: str
    email: EmailStr
    password: str


class CreatedUser(BaseSchema):
    id: PydanticObjectId = Field(alias = "_id")
    name: str
    email: EmailStr

   