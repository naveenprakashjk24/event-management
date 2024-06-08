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