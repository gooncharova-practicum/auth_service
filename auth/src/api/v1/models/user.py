from uuid import UUID

from pydantic import BaseModel


class GetUserModel(BaseModel):
    login: str
    first_name: str
    last_name: str
    email: str
    is_active: bool
    is_deleted: bool

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_active: bool
    password: str

    class Config:
        orm_mode = True


class LoginHistory(BaseModel):
    user_id: UUID
    user_agent: str
    ip_address: str
    device_type: str

    class Config:
        orm_mode = True
