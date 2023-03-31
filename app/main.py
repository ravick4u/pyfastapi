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
from . import schema

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


@app.get("/v2/posts", response_model=List[schema.Post])
def v2_get_posts(db: Session = Depends(get_db)):
    '''Get all posts
    '''
    my_posts = db.query(models.Post).all()

    return my_posts


@app.post("/v2/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def v2_create_posts(newpost: schema.PostCreate, db: Session = Depends(get_db)):
    '''Create Posts
    '''

    new_post = models.Post(**newpost.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    print(new_post)
    return new_post


@app.get('/v2/posts/{id}', response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    '''Get single post'''

    return_post = db.query(models.Post).filter(models.Post.id == id).first()

    if return_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")
    else:
        return return_post


@app.delete('/v2/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    '''Delete post'''

    post_to_delete_query = db.query(models.Post).filter(models.Post.id == id)
    if post_to_delete_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")
    post_to_delete_query.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/v2/posts/{id}', response_model=schema.Post)
def update_post(id: int, update_post: schema.PostUpdate, db: Session = Depends(get_db)):
    '''Update Post'''

    update_post_query = db.query(models.Post).filter(models.Post.id == id)

    if update_post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")

    update_post_query.update(update_post.dict())
    db.commit()

    return update_post_query.first()


@app.get("/")
async def root():
    '''Root function
    '''
    return {"message": "hello world!!!"}


@app.get("/posts")
def get_posts():
    '''Get all posts
    '''
    try:
        # Connect to an existing database
        # /* eslint-disable-line not -context-manager * /
        with psycopg.connect(postgres_connection_string) as conn:

            # Open a cursor to perform database operations
            with conn.cursor() as cur:
                print("connection succss")
                cur.execute("""
                    SELECT * FROM posts
                    """)
                my_posts = cur.fetchall()
    except:
        print("Connection failed")
    return my_posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(newpost: schema.PostCreate):
    '''Create Posts
    '''

    return_post = None

    try:
        # Connect to an existing database
        # /* eslint-disable-line not -context-manager * /
        with psycopg.connect(postgres_connection_string) as conn:

            # Open a cursor to perform database operations
            with conn.cursor() as cur:
                print("connection succss")
                cur.execute("""
                    INSERT INTO posts(title,content,published) VALUES (%s, %s, %s) RETURNING *
                    """, (newpost.title, newpost.content, newpost.published))
                return_post = cur.fetchone()
                conn.commit()

    except Exception as ex:
        print("Connection failed", ex)

    return return_post


@app.get('/posts/{id}')
def get_post(id: int):
    '''Get single post'''

    return_post = None

    try:
        # Connect to an existing database
        # /* eslint-disable-line not -context-manager * /
        with psycopg.connect(postgres_connection_string) as conn:

            # Open a cursor to perform database operations
            with conn.cursor() as cur:
                print("connection succss")
                cur.execute("""
                    SELECT * FROM posts WHERE id = %s
                    """, (id,))
                return_post = cur.fetchone()

    except Exception as ex:
        print("Connection failed", ex)

    if return_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")
    else:
        return return_post


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    '''Delete post'''

    post_to_delete = None
    try:
        # Connect to an existing database
        # /* eslint-disable-line not -context-manager * /
        with psycopg.connect(postgres_connection_string) as conn:

            # Open a cursor to perform database operations
            with conn.cursor() as cur:
                print("connection succss")
                cur.execute("""
                    DELETE FROM posts WHERE id = %s RETURNING *
                    """, (id,))
                post_to_delete = cur.fetchone()
                # conn.execute()

    except Exception as ex:
        print("Connection failed", ex)

    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, update_post: schema.PostUpdate):
    '''Update Post'''
    return_post = None

    try:
        # Connect to an existing database
        # /* eslint-disable-line not -context-manager * /
        with psycopg.connect(postgres_connection_string) as conn:

            # Open a cursor to perform database operations
            with conn.cursor() as cur:
                print("connection succss")
                cur.execute("""
                    UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
                    """, (update_post.title, update_post.content, update_post.published, id))
                return_post = cur.fetchone()
                conn.commit()

    except Exception as ex:
        print("Connection failed", ex)

    if return_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")

    return return_post


@app.get("/users", response_model=List[schema.User])
def get_all_users(db: Session = Depends(get_db)):
    '''Get all Users
    '''
    all_users = db.query(models.User).all()

    return all_users


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.User)
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


@app.put('/users/{id}', response_model=schema.User)
def update_user(id: int, update_post: schema.UserUpdate, db: Session = Depends(get_db)):
    '''Update User'''

    update_user_query = db.query(models.User).filter(models.User.id == id)

    if update_user_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} not found")

    update_user_query.update(update_post.dict())
    db.commit()

    return update_user_query.first()


@app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    '''Delete user'''

    user_to_delete_query = db.query(models.User).filter(models.User.id == id)
    if user_to_delete_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} not found")
    user_to_delete_query.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get('/user/{id}', response_model=schema.User)
def get_post(id: int, db: Session = Depends(get_db)):
    '''Get single User'''

    return_user = db.query(models.User).filter(models.User.id == id).first()

    if return_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} not found")
    else:
        return return_user
