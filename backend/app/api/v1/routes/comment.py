from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.comment import Comment

router = APIRouter()


@router.get("/comments")
def get_comments(db: Session = Depends(get_db)):
    return db.query(Comment).all()


@router.post("/comments")
def create_comment(content: str, post_id: int, user_id: int, db: Session = Depends(get_db)):
    comment = Comment(content=content, post_id=post_id, user_id=user_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment