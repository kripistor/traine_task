from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.models.user import User


class UserCreate(BaseModel):
    surname: str
    name: str
    middle_name: str
    login: str
    password: str

    class Config:
        orm_mode = True


class UserUpdate(UserCreate):
    pass


class UserRead(UserCreate):
    id: int


class UserLogin(BaseModel):
    login: str
    password: str

    class Config:
        orm_mode = True
