from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.models.post import Post
from app.schemas.post import PostSchema, PostCreate, PostUpdate, PostWithUserSchema


router = APIRouter()

@router.get("/posts", response_model=List[PostSchema])
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

@router.get("/posts/{post_id}", response_model=PostWithUserSchema)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pots with ID {post_id} not found"
        )
    return post


@router.post("/posts", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, user_id: int, db: Session = Depends(get_db)):
    db_post = Post(
        user_id=user_id,
        title=post.title,
        content=post.content,
        image_url=post.image_url,
        visibility=post.visibility
    )

    db.add(db_post)
    db.commit()
    db.refresh()
    return db_post


@router.put("/posts/{post_id}", response_model=PostSchema)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} not found"
        )

    update_data = post_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} not found"
        )

    db.delete(db_post)
    db.commit()
    return None


@router.get("/users/{user_id}/posts", response_model=List[PostSchema])
def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    return posts