from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class CommentBase(BaseModel):
    content: str
    post_id: int
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentSchema(CommentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CommentWithUserSchema(CommentSchema):
    user: 'UserSchema'

    model_config = ConfigDict(from_attributes=True)

class CommentWithRepliesSchema(CommentSchema):
    replies: List["CommentWithRepliesSchema"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

from app.schemas.user import UserSchema