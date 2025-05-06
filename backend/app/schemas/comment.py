from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from typing import ForwardRef

CommentWithRepliesRef = ForwardRef('CommentWithRepliesSchema')

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
        from_attributes = True

class CommentWithUserSchema(CommentSchema):
    user: 'UserSchema'

    class Config:
        from_attributes = True

class CommentWithRepliesSchema(CommentSchema):
    replies: List[CommentWithRepliesRef] = []

    class Config:
        from_attributes = True

CommentWithRepliesSchema.model_rebuild()

from app.schemas.user import UserSchema