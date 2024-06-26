from os import name
from typing import List
from zoneinfo import available_timezones

import database
import models
import schemas
from auth import oauth2
from fastapi import APIRouter, Depends, HTTPException, status
from h11 import Event
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/event',
    tags=['Events']
)

@router.get('/list',response_model=List[schemas.EventList])
def all_events(db: Session = Depends(database.get_db),current_user:schemas.Event = Depends(oauth2.get_current_user)):
    events = db.query(models.Event).all()
    return events

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.BaseEvent)
def create_event(request:schemas.Event, db: Session = Depends(database.get_db),
                 current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):

    if request.available_tickets <=0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Enter ticket counts greater than 0.")

    if request.price <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Enter ticket price greater than 0.")

    admin_user =  db.query(models.User).filter(models.User.id == current_user.get('id')).first()

    if admin_user.is_admin:
        new_event = models.Event(name=request.name, description=request.description, location= request.location, available_tickets= request.available_tickets, price=request.price, user_id=current_user.get('id'))
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return new_event
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User don't have a permission to create an event")

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Event)
def event_info(id:int, db: Session = Depends(database.get_db), current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):
    event = db.query(models.Event).filter(models.Event.id == id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Event Not found')
    return event

@router.post('/book-ticket', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBooking)
def book_ticket(request:schemas.BookingTicket, db: Session = Depends(database.get_db),
                current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):

    event=db.query(models.Event).filter(models.Event.id==request.event_id).first()
    print(event)
    if event is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Event not available')
    if event.available_tickets==0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Tickets not available')
    elif event.available_tickets < request.ticket:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{event.available_tickets} tickets only available')
    elif event.available_tickets>=request.ticket:
        price_calc = event.price * request.ticket
        ticket_cal = event.available_tickets - request.ticket
        new_booking = models.Ticket(user_id=current_user.get('id'),event_id= request.event_id, price=price_calc, ticket=request.ticket)
        db.query(models.Event).filter(models.Event.id==request.event_id).update({models.Event.available_tickets:ticket_cal})
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return new_booking

@router.patch('/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_event(id:int, request:schemas.UpdateEvent, db:Session=Depends(database.get_db),
                 current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):
    event = db.query(models.Event).filter(models.Event.id == id)

    if not event.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Event Not found')

    admin_user =  db.query(models.User).filter(models.User.id == current_user.get('id')).first()
    if admin_user.is_admin:
        event.update({
            models.Event.name : event.first().name,
            models.Event.description : event.first().description,
            models.Event.location : event.first().location,
            models.Event.available_tickets : request.available_tickets,
            models.Event.price : request.price
        })
        db.commit()
        return {'detail': 'event updated'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User don't have a permission to update an event")

@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def delete_event(id:int, db: Session = Depends(database.get_db),
                 current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):

    event=db.query(models.Event).filter(models.Event.id== id)
    if event.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Event not available')
    admin_user =  db.query(models.User).filter(models.User.id == current_user.get('id')).first()
    if admin_user.is_admin:
        event.delete(synchronize_session=False)
        db.commit()
        return {'detail': 'event deleted successfully'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User don't have a permission to delete an event")