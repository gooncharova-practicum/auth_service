from pydantic import UUID4, BaseModel, validator
from src.core import errors


class BaseRole(BaseModel):
    name: str
    description: str

    @validator("name")
    def len_of_role_name(cls, value):
        param = "name"
        if len(value) > 32:
            raise errors.LenOfValueError(param, 32, big=True)
        return value

    @validator("description")
    def len_of_description(cls, value):
        param = "description"
        if len(value) > 200:
            raise errors.LenOfValueError(param, 200, big=True)
        return value


class NewRole(BaseRole):
    name: str
    description: str | None


class UpdatedRole(BaseRole):
    name: str | None
    description: str | None


class Role(BaseModel):
    uid: UUID4
    name: str
    descripton: str | None
