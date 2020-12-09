from dataclasses import dataclass
from datetime import datetime
from importlib import import_module
from os.path import dirname, join
#from PIL import Image
from pytz import timezone
from shutil import copyfileobj
from typing import List
from cv2 import cv2
import io
import json
import logging
import os
import pytz
import sys

from fastapi import APIRouter, Depends, FastAPI, File, Form, Header, HTTPException, Request, Response, UploadFile
from fastapi.responses import FileResponse
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.orm import Session

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
# Post Blog
# Author Using Only
@router.post("/{uuid}/post",
            response_model=schemas.Post,
            summary="Post Blog",
)
def post_blog(uuid: str,blog: schemas.PostCreate, db: Session = Depends(get_db)):
   
    # Logging
    logger.info("Post Blog - parameters: uuid={}, blog={}".format(uuid,blog))

    # Check if there exists a match in UUID table
    uuid_record = crud.get_author_by_uuid(db, uuid=uuid)
    if uuid_record is None:
        raise HTTPException(status_code=404, detail="UUID not found")

    upload_blog = crud.post_blog(uuid=uuid,blog=blog,db=db)
    return upload_blog
  
@router.get("/{uuid}",
            response_model=List[schemas.Post],
            summary="Get Blog From Author",
)
def get_blog_from_uuid(uuid: str, db: Session = Depends(get_db)):
    db_blog = crud.get_blog_from_author(db=db, uuid=uuid)
    if db_blog:
        return crud.get_blog_from_author(db=db,uuid=uuid)
    else: 
        raise HTTPException(status_code=404, detail="Blog not found")

@router.get("/{id}/{uuid}",
            response_model=schemas.Post,
            summary= "Get Blog from uuid,Id",
)

def get_blog_from_id(id: int,uuid: str, db: Session = Depends(get_db)):
    # Logging
    logger.info("Get Blog - parameters: id={}".format(id))
 
    db_blog = crud.get_blog_from_id(db=db,id=id,uuid=uuid)
    if db_blog:
        return db_blog
    raise HTTPException(status_code=404, detail="Blog not found")

