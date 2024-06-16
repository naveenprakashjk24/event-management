from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Event(BaseModel):
    name : str
    description : str
    location : str
    price: Decimal
    available_tickets : int

class EventList(BaseModel):
    id: int
    name : str
    description : str
    location : str
    price: Decimal
    available_tickets : int

class UpdateEvent(BaseModel):
    price: Decimal
    available_tickets : int

class BaseEvent(Event):
    name: str
    description: str
    location: str
    price: Decimal
    available_tickets: int
    created_on : datetime
    class Config():
        from_attributues = True


class Booking(BaseModel):
    user_id : int
    event_id : int
    ticket:int
    price: Decimal

class BookingTicket(BaseModel):
    event_id: int
    ticket:int

class ShowBooking(Booking):
    user_id: int
    event_id : int
    ticket:int
    price: Decimal
    created_on: datetime
    class Config():
        from_attributues = True


class User(BaseModel):
    name: str
    email: str
    password : str
    is_admin : int


class ShowUser(BaseModel):
    name: str
    email: str
    is_admin : int
    class Config():
        from_attributes = True
