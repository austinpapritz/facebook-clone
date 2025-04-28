from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app.db.base import Base


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fastapi:fastapi@db:5432/facebook_clone")


engine = create_engine(DATABASE_URL, future=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)