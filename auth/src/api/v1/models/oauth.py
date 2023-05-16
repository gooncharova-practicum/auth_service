from pydantic import UUID4, BaseModel, EmailStr, Field, validator


class YandexUser(BaseModel):
    id: str
    email: EmailStr = Field(alias="default_email")
    login: str
    display_name: str
    emails: list[EmailStr]
    first_name: str
    last_name: str
    real_name: str
    sex: str
    social_name: str = "yandex"


class GoogleToken(BaseModel):
    sub: str
    email: EmailStr
    email_verified: bool
