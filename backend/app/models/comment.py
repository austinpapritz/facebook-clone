from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime 
from app.db.base import Base

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey="users.id", nullable=False)
    post_id = Column(Integer, ForeignKey="posts.id", nullable=False)
    content = Column(String, nuullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    user = relationship("User")
    post = relationship("Post", backref="comments")