'''Main file
'''
# pylint: skip-file

from msilib import type_nullable
from random import randrange
from typing import List, Optional
from typing_extensions import deprecated
from urllib import response
from fastapi import Depends, FastAPI, Response, status, HTTPException
import psycopg

from app import util
# from psycopg.cursor import RealDictCursor
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .routers import post, user


models.Base.metadata.create_all(bind=engine)
# Dependency


app = FastAPI()

# try:
#     conn = psycopg.connect("host=localhost port=5432 dbname=postgres")
# except:
#     pass

postgres_connection_string = "dbname=postgres user=postgres password=***"


def test_connection():
    try:
        # Connect to an existing database
        # /* eslint-disable-line not -context-manager * /
        with psycopg.connect(postgres_connection_string) as conn:

            # Open a cursor to perform database operations
            with conn.cursor() as cur:

                print("connection succss")
    except:
        print("Connection failed")


test_connection()


my_posts = [
    {
        "title": "Post title1",
        "content": "Post content1",
        "published": False,
        "rating": None,
        "id": 1
    }
]


@app.get('/testsqlalchemy')
def testsqlalchemy(db: Session = Depends(get_db)):
    all_posts = db.query(models.Post).all()
    return all_posts


@app.get("/")
async def root():
    '''Root function
    '''
    return {"message": "hello world!!!"}

app.include_router(post.router)
app.include_router(user.router)
