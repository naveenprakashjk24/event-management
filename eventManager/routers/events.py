import datetime
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

@router.get('/list',response_model=List[schemas.Event])
def allEvents(db: Session = Depends(database.get_db),current_user:schemas.Event = Depends(oauth2.get_current_user)):
    events = db.query(models.Event).all()
    return events

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.BaseEvent)
def createEvent(request:schemas.Event, db: Session = Depends(database.get_db), current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):

    if current_user.get('is_admin'):
        new_event = models.Event(name=request.name, description=request.description, location= request.location, available_tickets= request.available_tickets,event_expiry_on= request.event_expiry_on,  user_id=current_user.get('id'))
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return new_event
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User don't have a permission to create an event")
