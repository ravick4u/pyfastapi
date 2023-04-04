from tkinter import RAISED
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database, schema, models, util, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user_credentials: schema.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials1')
    if not util.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials2')

    access_token = oauth2.create_access_token(data={"user_id": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
