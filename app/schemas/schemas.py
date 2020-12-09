# Pydantic model
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel
import enum
import operator
import sqlalchemy.types as types

# Class
# Author
class AuthorBase(BaseModel):
    name: str
    uuid: str


class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    
    class Config:
        orm_mode = True

# Post
class PostBase(BaseModel):
    content: str
    name: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id : int
    author: str
    class Config:
        orm_mode = True

# Comment
class CommentBase(BaseModel):
    comment: Optional[str] = None

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    id_commentor: int
    id_post: int

    class Config:
        orm_mode = True

# Commentor
class CommentorBase(BaseModel):
    name: str
    
class CommentorCreate(CommentorBase):
    pass

class Commentor(CommentorBase):
    id: int
    class Config:
        orm_mode = True

