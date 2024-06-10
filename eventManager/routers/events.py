from typing import List

import database
import models
import schemas
from auth import oauth2
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/event',
    tags=['Events']
)

@router.get('/list',response_model=List[schemas.EventList])
def allEvents(db: Session = Depends(database.get_db),current_user:schemas.Event = Depends(oauth2.get_current_user)):
    events = db.query(models.Event).all()
    return events

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.BaseEvent)
def createEvent(request:schemas.Event, db: Session = Depends(database.get_db), current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):

    if current_user.get('is_admin'):
        new_event = models.Event(name=request.name, description=request.description, location= request.location, available_tickets= request.available_tickets, price=request.price, user_id=current_user.get('id'))
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return new_event
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User don't have a permission to create an event")

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Event)
def eventInfo(id:int, db: Session = Depends(database.get_db)):
    event = db.query(models.Event).filter(models.Event.id == id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Event Not found')
    return event

@router.post('/book-ticket', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBooking)
def bookTicket(request:schemas.BookingTicket, db: Session = Depends(database.get_db), current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):

    event=db.query(models.Event).filter(models.Event.id==request.event_id).first()
    price_calc = event.price * request.ticket
    ticket_cal = event.available_tickets - request.ticket
    if event.available_tickets==0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Tickets not available')
    elif event.available_tickets < request.ticket:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{event.available_tickets} tickets only available')
    elif event.available_tickets>=request.ticket:
        new_booking = models.Ticket(user_id=current_user.get('id'),event_id= request.event_id, price=price_calc, ticket=request.ticket)
        db.query(models.Event).filter(models.Event.id==request.event_id).update({models.Event.available_tickets:ticket_cal})
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return new_booking
