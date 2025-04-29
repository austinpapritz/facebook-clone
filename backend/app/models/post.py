from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base

class VisibilityType(str, enum.Enum):
    PUBLIC = "public"
    FRIENDS = "friends"
    PRIVATE = "private"


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=True)
    content = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    visibility = Column(Enum(VisibilityType), default=VisibilityType.PUBLIC)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    user = relationship("User", backref="posts")