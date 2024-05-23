from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    title: str
    description: str
    date: datetime

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    users: List[User] = []

    class Config:
        orm_mode = True
