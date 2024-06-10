from typing import List

import database
import models
import schemas
from auth.hashing import Hash
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/user-',
    tags=['Users']
)

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def createUser(request:schemas.User, db: Session = Depends(database.get_db)):

    new_user = models.User(name=request.name, email= request.email, password = Hash.bcrypt(request.password), is_admin=request.is_admin)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/list', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def userList(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users

# @router.get('/{id}', response_model=schemas.ShowUserBlog)
# def user(id:int, db: Session = Depends(database.get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=' User Not found')
#     return user