from pydantic import BaseModel


class ApiV1Config(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"
