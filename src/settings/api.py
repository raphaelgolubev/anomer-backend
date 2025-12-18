from pydantic import BaseModel


class ApiV1Config(BaseModel):
    prefix: str = "/v16_12_2025"
    auth: str = "/auth"
    users: str = "/users"
