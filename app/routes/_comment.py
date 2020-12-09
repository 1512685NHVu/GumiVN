from datetime import datetime
from pytz import timezone
from typing import List
import logging
import os
import pytz
import sys

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Request, Response
from loguru import logger
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from App_Blog.app.models import models
from App_Blog.app import crud
from App_Blog.app import logConfig
from App_Blog.app.schemas import schemas

# API
router = APIRouter()

# LOGGING
# set loguru format for root logger
logging.getLogger().handlers = [logConfig.InterceptHandler()]

# set format
logger.configure(
    handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": logConfig.format_record}]
)

logging.getLogger("uvicorn.access").handlers = [logConfig.InterceptHandler()]

# Dependency
def get_db(request: Request):
    return request.state.db

# API Methods
@router.post("/", 
             response_model=schemas.Comment,
             summary="Create Commentor",
)
def comment_create(id_post:int,id_commentor:int,comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    check_commentorID = crud.get_commentor_byID(db=db,id=id_commentor)
    check_postID=crud.get_blog_from_idd(db=db,id=id_post)
    if check_commentorID and check_postID:
        return crud.comment_create(db=db, comment=comment,id_post=id_post,id_comment=id_commentor)
    raise HTTPException(status_code=404, detail="User/Post not found")

@router.get("post/{id_post}",
            response_model=List[schemas.Comment],
            summary="Get All Comment List By ID Post ",
            )
def get_comment_byIDPost(id_post:int,db: Session = Depends(get_db)):
    return crud.fetch_all_comment_from_post(db=db,id_post=id_post)

@router.get("commentor/{id_commentor}",
            response_model=List[schemas.Comment],
            summary="Get All Comment List By Commentor ",
            )
def get_comment_byCommentor(id_commentor:int,db: Session = Depends(get_db)):
    return crud.fetch_all_comment_from_commentor(db=db,id_commentor=id_commentor)

# Delete Comment By ID
@router.delete("/deletecomment/{comment_id}")
def delete_file(comment_id:int,db: Session = Depends(get_db)):
    comment_id = crud.get_comment_byID(db=db,id=comment_id)
    if comment_id:
        db.delete(comment_id)
        db.commit()
        return ('Deleted Success')
    else:
        raise HTTPException(status_code=404, detail="Comment does not exist")

# Update Comment
@router.patch("/updatecomment/{comment_id}",
             response_model = schemas.Comment   
                )
def update_comment(comment_id:int,cmt_in: schemas.CommentCreate,db: Session = Depends(get_db)):
    comment_check = crud.get_comment_byID(db=db,id=comment_id)
    if not comment_check:
        raise HTTPException(status_code=404,detail="Comment does not exist")
    cmt_check_json_data = jsonable_encoder(comment_check)
    cmt_check_json = schemas.Comment(**cmt_check_json_data)
    update_cmt = cmt_check_json.copy(update=cmt_in.dict())
    data = jsonable_encoder(update_cmt)
    updated_cmt = models.Comment(**data)

    db.merge(updated_cmt)
    db.flush()
    db.commit()
    return updated_cmt

  

