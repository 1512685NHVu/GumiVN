# SQLAlchemy Model

from datetime import datetime
from datetime import timezone

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, JSON, String,Table
from sqlalchemy.orm import relationship, backref
from App_Blog.app.database.database import Base


# association_table = Table('association', Base.metadata,
#     Column('commentor_id', Integer, ForeignKey('commentor.id')),
#     Column('post_id', Integer, ForeignKey('post.id'))
# )


# Author table
class Author(Base):
    __tablename__ = "author"

    uuid = Column(String, primary_key=True, index=True)
    # uuid = Column(String,index = True)
    name = Column(String, index = True)
    post = relationship("Post",backref="author_post",passive_deletes=True)
# Post table
class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    author = Column(Integer,ForeignKey("author.uuid"), index=True)
    name = Column(String, index= True)
    commentors = relationship('Commentor', secondary='comment',backref="post")
    comment= relationship('Comment',backref="post_comment",passive_deletes=True)

# Comment table
class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, index=True)
    id_commentor = Column(Integer,ForeignKey("commentor.id"), index=True)
    id_post = Column(Integer,ForeignKey("post.id"), index=True)


# Commentor table
class Commentor(Base):
    __tablename__ = "commentor"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    posts = relationship('Post', secondary='comment',backref="commentor")
    comment = relationship('Comment',backref = 'commentor_com',passive_deletes=True)
    

# Commentor - Post table (Many2many)
# class CommentorPost(Base):
#     __tablename__= "commentor_post"
#     commentor_id = Column(Integer, ForeignKey('commentor.id'), primary_key=True)
#     post_id = Column(Integer, ForeignKey('post.id'), primary_key=True)
