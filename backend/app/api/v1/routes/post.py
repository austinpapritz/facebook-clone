from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.post import Post

router = APIRouter()

@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()