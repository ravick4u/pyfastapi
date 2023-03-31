'''Main file
'''
# pylint: skip-file

from msilib import type_nullable
from random import randrange
from typing import Optional
from urllib import response
from fastapi import Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg
# from psycopg.cursor import RealDictCursor
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

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


class Post(BaseModel):
    '''Post Class'''
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {
        "title": "Post title1",
        "content": "Post content1",
        "published": False,
        "rating": None,
        "id": 1
    }
]


@app.route('/testsqlalchemy')
def testsqlalchemy(db: Session = Depends(get_db)):
    return {"status": "success"}


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
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(newpost: Post):
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

    return {"data": return_post}


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
        return {"data": return_post}


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
def update_post(id: int, update_post: Post):
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

    return {
        "data": return_post
    }
