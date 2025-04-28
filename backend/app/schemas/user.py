from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Base User Schema with shared attributes
class UserBase(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_active: bool = True
    role: str = "user"


# Schema for creating a user
class UserCreate(UserBase):
    password: str


# Schema for updating a user
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_active: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None


# Schema for DB representation (includes all fields including ids and timestamps)
class UserInDB(UserBase):
    id: int
    password_hash: str
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


    class Config:
        orm_mode = True


# Schema returned to client (excludes sensitive data)
class UserSchema(UserBase):
    id: int
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


    class Config:
        orm_mode = True