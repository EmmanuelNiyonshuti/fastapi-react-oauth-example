from pydantic import BaseModel, ConfigDict, SecretStr


class UserIn(BaseModel):
    username: str
    email: str
    password: SecretStr


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uid: int
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"
