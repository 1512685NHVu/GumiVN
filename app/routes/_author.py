from typing import List
import logging
import os
import sys

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Request, Response
from loguru import logger
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


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
@router.post('/authorCreate/', status_code=201,
             response_model=schemas.Author,
             summary="Author Create")

def author_create(author: schemas.AuthorCreate,db: Session = Depends(get_db)):
    # Logging
    logger.info("Create CameraParams - parameters: author={}".format(author))
    return crud.author_create(db=db, author=author)

@router.get("/{uuid}", 
            response_model=schemas.Author,
            summary="GET Author Infor",
)
def get_author_byUuid(uuid: str, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_uuid(db, uuid=uuid)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    # Logging
    logger.info("Fetch Author - result:")
    logger.info("name={}".format(db_author.name))
    return db_author

@router.get("/",
            response_model= List[schemas.Author],
            summary="Get Author List"
            )
def get_authors(db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db)
    return db_author
    

