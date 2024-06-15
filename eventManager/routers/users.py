import re
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
import models
import schemas
from auth.hashing import Hash

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def checkEmail(email):

    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def createUser(request:schemas.User, db: Session = Depends(database.get_db)):

    if not checkEmail(request.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid email address')

    user=db.query(models.User).filter(models.User.email==request.email).first()

    if user is None:
        new_user = models.User(name=request.name, email= request.email, password = Hash.bcrypt(request.password), is_admin=request.is_admin)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email address already exist.')


@router.get('/list', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def userList(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users
