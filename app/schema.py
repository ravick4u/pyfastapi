from pydantic import BaseModel


class PostBase(BaseModel):
    '''Post Class'''
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass
