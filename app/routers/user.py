# pylint: skip-file

from typing import List

from .. import schema
from .. import models, util
from fastapi import Depends, Response, status, HTTPException, APIRouter
import psycopg
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal, get_db
import sys

router = APIRouter()


@router.get("/users", response_model=List[schema.User])
def get_all_users(db: Session = Depends(get_db)):
    '''Get all Users
    '''
    all_users = db.query(models.User).all()

    return all_users


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_user(newuser: schema.UserCreate, db: Session = Depends(get_db)):
    '''Create User
    '''

    # hash the password
    hashed_password = util.hash(newuser.password)
    newuser.password = hashed_password
    new_user = models.User(**newuser.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print(new_user)
    return new_user


@router.put('/users/{id}', response_model=schema.User)
def update_user(id: int, update_user: schema.UserUpdate, db: Session = Depends(get_db)):
    '''Update User'''

    update_user_query = db.query(models.User).filter(models.User.id == id)

    if update_user_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} not found")

    hashed_password = util.hash(update_user.password)
    print('hashed')
    print(hashed_password)
    update_user.password = hashed_password

    update_user_query.update(update_user.dict())
    db.commit()

    return update_user_query.first()


@router.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    '''Delete user'''

    user_to_delete_query = db.query(models.User).filter(models.User.id == id)
    if user_to_delete_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} not found")
    user_to_delete_query.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/user/{id}', response_model=schema.User)
def get_user(id: int, db: Session = Depends(get_db)):
    '''Get single User'''

    return_user = db.query(models.User).filter(models.User.id == id).first()

    if return_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} not found")
    else:
        return return_user
