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
             response_model=schemas.Commentor,
             summary="Create Commentor",
)
def post_uuid(commentor: schemas.CommentorCreate, db: Session = Depends(get_db)):
 
    # Logging
    logger.info("Create Commentor - parameters: {}".format(commentor))
    return crud.create_commentor(db=db, commentor=commentor)

@router.get("/{id_post}",
            response_model=List[schemas.Comment],
            summary="Get Commentor List By ID Post ",
            )
def get_commentor_byIDPost(id_post:int,db: Session = Depends(get_db)):
    return crud.fetch_all_commentor_from_post(db=db,id_post=id_post)


