from typing import List

from pydantic import BaseModel


class Event(BaseModel):

    name : str
    description : str
    location : str
    available_tickets : int
    created_on : str
    event_expiry_on : str


class User(BaseModel):
    name: str
    email: str
    password : str

class UserBase(User):
    name: str
    email: str
    class Config():
        from_attributes = True

class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        from_attributes = True
