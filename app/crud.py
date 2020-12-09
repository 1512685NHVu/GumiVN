from datetime import datetime
import json
from fastapi import HTTPException

from sqlalchemy import func
from sqlalchemy.orm import Session,join

from App_Blog.app.models import models
from App_Blog.app.schemas import schemas

# Author
def author_create(db: Session, author: schemas.AuthorCreate):
    ## Check if database already had a record for this UUID.
    check = db.query(models.Author).filter(models.Author.uuid == author.uuid).first()
    if check:

        raise HTTPException(status_code=404, detail="UUID existed already")

    #currentDate = uuid.createdAt.strftime("%d/%m/%Y %H:%M:%S")
    db_author = models.Author(
        uuid = author.uuid,
        name = author.name,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_author_by_uuid(db:Session, uuid: str):
    return db.query(models.Author).filter(models.Author.uuid==uuid).first()

def get_author(db:Session):
    return db.query(models.Author).all()

# Post

def post_blog(db: Session,blog: schemas.PostCreate,uuid : str):
    temp = get_author_by_uuid(db=db,uuid=uuid)
    db_blog = models.Post(
        content=blog.content,
        name= blog.name,
        author = temp.uuid
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blog_from_author(db: Session,uuid: str):
    # return db.query(models.Post).join(models.Author).filter(models.Author.uuid== id_post).all()
    return db.query(models.Post).filter(models.Post.author==uuid).all()

def get_blog_from_id(db: Session,id: int,uuid:str):
    return db.query(models.Post).filter_by(author = uuid, id = id).first()
def get_blog_from_idd(db:Session,id:int):
    return db.query(models.Post).filter(models.Post.id==id).first()
#Commentor

def create_commentor(db: Session,commentor: schemas.CommentorCreate):
    print(db.query(models.Commentor).filter(models.Commentor.posts))
    db_commentor = models.Commentor(
        name = commentor.name,
    )
    db.add(db_commentor)
    db.commit()
    db.refresh(db_commentor)
    return db_commentor

def get_commentor_byID(db: Session,id:int):
    return db.query(models.Commentor).filter(models.Commentor.id==id).first()
def fetch_all_commentor_from_post(db: Session,id_post: int):
    return db.query(models.Comment).filter(models.Commentor.posts and models.Comment.id_post==id_post).all()

#Comment
def comment_create(db: Session, comment: schemas.CommentCreate,id_post:int,id_comment:int):
    commentor_id = get_commentor_byID(db=db,id=id_comment)
    db_comment= models.Comment(
        comment = comment.comment,
        id_post = id_post,     
        id_commentor = commentor_id.id      
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def fetch_all_comment_from_post(db:Session,id_post:int):
    return db.query(models.Comment).join(models.Post).filter(models.Post.id==id_post).all()
    
def fetch_all_comment_from_commentor(db:Session,id_commentor:int):
    return db.query(models.Comment).join(models.Commentor).filter(models.Commentor.id==id_commentor).all()

def get_comment_byID(db:Session,id:int):
    return db.query(models.Comment).filter(models.Comment.id==id).first()

# def update_comment(db: Session,cmt_in: schemas.CommentBase):
#         obj_data = jsonable_encoder(db_obj)
#         if isinstance(obj_in, dict):
#             update_data = obj_in
#         else:
#             update_data = obj_in.dict(exclude_unset=True)
#         for field in obj_data:
#             if field in update_data:
#                 setattr(db_obj, field, update_data[field])
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj


   

