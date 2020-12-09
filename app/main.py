# Internal Python
from pprint import pformat
import logging
import os
import sys
# 3rd party
from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response
from loguru import logger
from loguru._defaults import LOGURU_FORMAT
from sqlalchemy.orm import Session

# Local packages
from App_Blog.app import crud
from App_Blog.app.models import models
from App_Blog.app.database.database import SessionLocal, engine
from App_Blog.app.routes import _author, _comment, _commentor, _post

models.Base.metadata.create_all(bind=engine)



# API
app = FastAPI()

parent_dir = "App_Blog/app/logs"
dir = "Blog-API-log"
path = os.path.join(parent_dir, dir)
logger.add(path, rotation="12:00", enqueue=True, encoding="utf8")

# Middleware
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Dependency
def get_db(request: Request):
    return request.state.db

# Methods

# Author
app.include_router(
    _author.router,
    prefix="/author",
    tags=["author"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Author Not Found"}},
)

#Comment
app.include_router(
    _comment.router,
    prefix="/comment", 
    tags=["comment"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Comment Not Found"}},
)

# Commentor
app.include_router(
    _commentor.router,
    prefix="/commentor",
    tags=["commentor"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Commentor Not Found"}},
)

# Post
app.include_router(
    _post.router,
    prefix="/post",
    tags=["post"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Post Not Found"}},
)