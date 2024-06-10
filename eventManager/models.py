import datetime

from database import Base
from sqlalchemy import (Boolean, Column, DateTime, Double, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship


class Event(Base):

    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    location = Column(String)
    available_tickets = Column(Integer)
    price = Column(Double, default=0.0)
    created_on = Column(DateTime, default=datetime.datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('User', back_populates='events')
    tickets = relationship('Ticket', back_populates='event')

class Ticket(Base):

    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('events.id'))
    ticket = Column(Integer, default=0)
    price = Column(Double, default=0.0)
    created_on = Column(DateTime, default=datetime.datetime.now())

    creator = relationship('User', back_populates='booking')
    event = relationship('Event', back_populates='tickets')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    events = relationship('Event', back_populates='creator')
    booking = relationship('Ticket', back_populates='creator')
