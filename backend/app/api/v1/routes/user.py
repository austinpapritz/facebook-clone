from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserSchema, UserCreate, UserUpdate, UserInDB
import hashlib


router = APIRouter()


@router.get("/users", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@router.post("/users", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
      (User.username == user.username) | (User.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail=f"Username or email already exists"
        )

    password_hash = hashlib.sha256(user.password.encode()).hexdigest()

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=password_hash,
        bio=user.bio,
        profile_image_url=user.profile_image_url,
        cover_image_url=user.cover_image_url,
        is_active=user.is_active,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/users/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    update_data = user_update.dict(exclude_unset=True)

    if "password" in update_data:
        password = update_data.pop("password")
        update_data["password_hash"] = hashlib.sha256(password.encode()).hexdigest()

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db_user.updated_at = datetime.now()

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    db.delete(db_user)
    db.commit()
    return None


@router.post("/user/{user_id}/login", response_model=UserSchema)
def login_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    user.last_login = datetime.now()
    db.commit()
    db.refresh(user)

    return user