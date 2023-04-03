from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    '''Post Base Class'''
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    '''Post Class to be used in Create'''
    pass


class PostUpdate(PostBase):
    '''Post class to be used in Update'''
    pass


class Post(PostBase):
    '''Post class to be used in returning data'''
    id: int
    created: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(BaseModel):
    id: int
    created: datetime

    class Config:
        orm_mode = True
