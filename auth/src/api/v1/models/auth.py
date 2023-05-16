from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr, Field, validator
from src.core import errors


class RegUserRequest(BaseModel):
    login: str
    first_name: str
    email: EmailStr
    password: str = Field(..., min_length=5, max_length=100)

    @validator("first_name")
    def len_of_first_name(cls, value):
        param = "first_name"
        if len(value) <= 5:
            raise errors.LenOfValueError(param, 5)
        elif len(value) > 150:
            raise errors.LenOfValueError(param, 150, big=True)
        return value


class LoginUserRequest(BaseModel):
    login: str
    password: str = Field(..., title="Password", min_length=5, max_length=100)


class TokenData(BaseModel):
    access_token: str
    access_token_expiration_date: datetime
    refresh_token: str
    refresh_token_expiration_date: datetime


class LogoutUser(BaseModel):
    refresh_token: str


class UserData(BaseModel):
    uid: UUID4
    login: str
    email: EmailStr


class JwtTokenModel(BaseModel):
    token: str
