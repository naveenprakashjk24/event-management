import datetime

from database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Event(Base):

    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    location = Column(String)
    available_tickets = Column(Integer)
    created_on = Column(DateTime, default=datetime.datetime.now())
    event_expiry_on = Column(DateTime, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('User', back_populates='events')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    events = relationship('Event', back_populates='creator')
