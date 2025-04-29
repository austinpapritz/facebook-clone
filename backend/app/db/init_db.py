from faker import Faker
from sqlalchemy.orm import Session
from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.db.session import SessionLocal
import hashlib

Base.metadata.create_all(bind=engine)

def seed_data(db: Session):
    fake = Faker()
    
    def generate_password_hash():
        password = fake.password(length=12)  # Plain password
        return hashlib.sha256(password.encode()).hexdigest()

    users = [User(username=fake.user_name(), email=fake.email(), password_hash=generate_password_hash()) for _ in range(5)]
    db.add_all(users)
    db.commit()

    posts = []
    for user in users:
        for _ in range(2):
            post = Post(content=fake.paragraph(), user_id=user.id)
            posts.append(post)
    db.add_all(posts)
    db.commit()

    comments = []
    for post in posts:
        for _ in range(3):
            comment = Comment(content=fake.sentence(), post_id=post.id, user_id=post.user_id)
            comments.append(comment)
    db.add_all(comments)
    db.commit()

def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    seed_data(db)
    db.close()
