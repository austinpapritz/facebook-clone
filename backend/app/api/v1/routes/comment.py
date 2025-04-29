from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.models.comment import Comment
from app.schemas.comment import CommentSchema, CommentCreate, CommentUpdate, CommentWithUserSchema, CommentWithRepliesSchema

router = APIRouter()

@router.get("/comments", response_model=List[CommentSchema])
def get_comments(db: Session = Depends(get_db)):
    return db.query(Comment).all()

@router.get("/comments/{comment_id}", response_model=CommentWithUserSchema)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {comment_id} not found"
        )
    return comment

@router.post("/comments", response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentCreate, user_id: int, db: Session = Depends(get_db)):
    # Create comment object
    db_comment = Comment(
        user_id=user_id,
        content=comment.content,
        post_id=comment.post_id,
        parent_id=comment.parent_id
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.put("/comments/{comment_id}", response_model=CommentSchema)
def update_comment(comment_id: int, comment_update: CommentUpdate, db: Session = Depends(get_db)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {comment_id} not found"
        )
    
    # Update content if provided
    if comment_update.content is not None:
        db_comment.content = comment_update.content
    
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {comment_id} not found"
        )
    
    db.delete(db_comment)
    db.commit()
    return None

@router.get("/posts/{post_id}/comments", response_model=List[CommentWithRepliesSchema])
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    # Get only top-level comments (no parent_id)
    comments = db.query(Comment).filter(
        Comment.post_id == post_id,
        Comment.parent_id == None
    ).all()
    return comments

@router.get("/comments/{comment_id}/replies", response_model=List[CommentSchema])
def get_comment_replies(comment_id: int, db: Session = Depends(get_db)):
    # Get direct replies to a comment
    replies = db.query(Comment).filter(Comment.parent_id == comment_id).all()
    return replies