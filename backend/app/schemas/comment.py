from pydantic import BaseModel
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

    class Config:
        orm_mode = True

class CommentWithUserSchema(CommentSchema):
    user: 'UserSchema'

    class Config:
        orm_mode = True

class CommentWithRepliesSchema(CommentSchema):
    replies: List['CommentWithRepliesSchema'] = []

    class Config:
        orm_mode = True

from app.schemas.user import UserSchema