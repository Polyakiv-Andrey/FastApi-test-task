from pydantic import BaseModel


class UserRegistrationsSchema(BaseModel):
    name: str
    username: str
    password: str
    confirm_password: str


class JWTTokens(BaseModel):
    access_token: str
    refresh_token: str
