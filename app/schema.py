from pydantic import BaseModel


class Post(BaseModel):
    '''Post Class'''
    title: str
    content: str
    published: bool = True
