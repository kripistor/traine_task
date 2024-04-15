from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.models.client import Client


class ClientCreate(BaseModel):
    account_number: int
    surname: str
    name: str
    middle_name: str
    birth_date: date
    itn: int
    status: str
    responsible_user_id: int

    class Config:
        orm_mode = True


class ClientUpdate(ClientCreate):
    pass


class ClientRead(ClientCreate):
    id: int
