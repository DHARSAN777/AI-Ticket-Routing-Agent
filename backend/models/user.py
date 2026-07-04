from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str
    name: str


class UserLogin(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime
    is_active: bool = True


class UserInDB(User):
    hashed_password: str