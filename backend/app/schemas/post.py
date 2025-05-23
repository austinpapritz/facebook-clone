from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

class VisibilityType(str, Enum):
    PUBLIC = "public"
    FRIENDS = "friends"
    PRIVATE = "private"

class PostBase(BaseModel):
    title: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    visibility: VisibilityType = VisibilityType.PUBLIC

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    visibility: Optional[VisibilityType] = None

class PostSchema(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PostWithUserSchema(PostSchema):
    user: 'UserSchema'

    model_config = ConfigDict(from_attributes=True)

from app.schemas.user import UserSchema