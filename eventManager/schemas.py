from datetime import datetime

from pydantic import BaseModel


class Event(BaseModel):

    name : str
    description : str
    location : str
    available_tickets : int
    created_on : datetime
    event_expiry_on : datetime

class BaseEvent(Event):
    name: str
    description: str
    location: str
    available_tickets: int
    created_on : datetime
    event_expiry_on: datetime
    class Config():
        from_attributues = True

class User(BaseModel):
    name: str
    email: str
    password : str
    is_admin : int

class UserBase(User):
    name: str
    email: str
    class Config():
        from_attributes = True

class ShowUser(BaseModel):
    name: str
    email: str
    is_admin : int
    class Config():
        from_attributes = True
