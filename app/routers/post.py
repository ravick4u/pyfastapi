# pylint: skip-file
from typing import List, Optional
from sqlalchemy.orm import Session
import psycopg
from fastapi import APIRouter, Depends, Response, status, HTTPException
from .. import models, schema, util
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    prefix="/v2/posts"
)


@router.get("/", response_model=List[schema.Post])
def v2_get_posts(db: Session = Depends(get_db)):
    '''Get all posts
    '''
    my_posts = db.query(models.Post).all()

    return my_posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def v2_create_posts(newpost: schema.PostCreate, db: Session = Depends(get_db)):
    '''Create Posts
    '''

    new_post = models.Post(**newpost.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    print(new_post)
    return new_post


@router.get('/{id}', response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    '''Get single post'''

    return_post = db.query(models.Post).filter(models.Post.id == id).first()

    if return_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")
    else:
        return return_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    '''Delete post'''

    post_to_delete_query = db.query(models.Post).filter(models.Post.id == id)
    if post_to_delete_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")
    post_to_delete_query.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schema.Post)
def update_post(id: int, update_post: schema.PostUpdate, db: Session = Depends(get_db)):
    '''Update Post'''

    update_post_query = db.query(models.Post).filter(models.Post.id == id)

    if update_post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")

    update_post_query.update(update_post.dict())
    db.commit()

    return update_post_query.first()


# @router.get("/posts")
# def get_posts():
#     '''Get all posts
#     '''
#     try:
#         # Connect to an existing database
#         # /* eslint-disable-line not -context-manager * /
#         with psycopg.connect(postgres_connection_string) as conn:

#             # Open a cursor to perform database operations
#             with conn.cursor() as cur:
#                 print("connection succss")
#                 cur.execute("""
#                     SELECT * FROM posts
#                     """)
#                 my_posts = cur.fetchall()
#     except:
#         print("Connection failed")
#     return my_posts


# @router.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(newpost: schema.PostCreate):
#     '''Create Posts
#     '''

#     return_post = None

#     try:
#         # Connect to an existing database
#         # /* eslint-disable-line not -context-manager * /
#         with psycopg.connect(postgres_connection_string) as conn:

#             # Open a cursor to perform database operations
#             with conn.cursor() as cur:
#                 print("connection succss")
#                 cur.execute("""
#                     INSERT INTO posts(title,content,published) VALUES (%s, %s, %s) RETURNING *
#                     """, (newpost.title, newpost.content, newpost.published))
#                 return_post = cur.fetchone()
#                 conn.commit()

#     except Exception as ex:
#         print("Connection failed", ex)

#     return return_post


# @router.get('/posts/{id}')
# def get_post(id: int):
#     '''Get single post'''

#     return_post = None

#     try:
#         # Connect to an existing database
#         # /* eslint-disable-line not -context-manager * /
#         with psycopg.connect(postgres_connection_string) as conn:

#             # Open a cursor to perform database operations
#             with conn.cursor() as cur:
#                 print("connection succss")
#                 cur.execute("""
#                     SELECT * FROM posts WHERE id = %s
#                     """, (id,))
#                 return_post = cur.fetchone()

#     except Exception as ex:
#         print("Connection failed", ex)

#     if return_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with {id} not found")
#     else:
#         return return_post


# @router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     '''Delete post'''

#     post_to_delete = None
#     try:
#         # Connect to an existing database
#         # /* eslint-disable-line not -context-manager * /
#         with psycopg.connect(postgres_connection_string) as conn:

#             # Open a cursor to perform database operations
#             with conn.cursor() as cur:
#                 print("connection succss")
#                 cur.execute("""
#                     DELETE FROM posts WHERE id = %s RETURNING *
#                     """, (id,))
#                 post_to_delete = cur.fetchone()
#                 # conn.execute()

#     except Exception as ex:
#         print("Connection failed", ex)

#     if post_to_delete is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with {id} not found")

#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put('/posts/{id}')
# def update_post(id: int, update_post: schema.PostUpdate):
#     '''Update Post'''
#     return_post = None

#     try:
#         # Connect to an existing database
#         # /* eslint-disable-line not -context-manager * /
#         with psycopg.connect(postgres_connection_string) as conn:

#             # Open a cursor to perform database operations
#             with conn.cursor() as cur:
#                 print("connection succss")
#                 cur.execute("""
#                     UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
#                     """, (update_post.title, update_post.content, update_post.published, id))
#                 return_post = cur.fetchone()
#                 conn.commit()

#     except Exception as ex:
#         print("Connection failed", ex)

#     if return_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with {id} not found")

#     return return_post
