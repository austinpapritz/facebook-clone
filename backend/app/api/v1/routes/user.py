from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.user import User

router = APIRouter()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
      return db.query(User).all()