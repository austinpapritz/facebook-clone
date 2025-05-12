import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from contextlib import asynccontextmanager

from app.db.base import Base
from app.main import app
from app.db.dependencies import get_db
from app.models.user import User
from app.models.post import Post, VisibilityType
from app.models.comment import Comment

TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Erase once real user data is used and handler is removed from main.py
@asynccontextmanager
async def test_lifespan(app):
    # No startup operations
    yield
    # No shutdown operations

# Override the lifespan for testing
@pytest.fixture(scope="session", autouse=True)
def override_lifespan():
    # Store original lifespan
    original_lifespan = app.router.lifespan_context
    
    # Replace with the test lifespan
    app.router.lifespan_context = test_lifespan
    
    yield
    
    # Restore original lifespan (if needed for cleanup)
    app.router.lifespan_context = original_lifespan

@pytest.fixture(scope="function")
def test_engine():
    engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys=ON"))
        conn.commit()

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_db(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(test_db):
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password",
        bio="Test bio",
        is_active=True,
        role="user"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_post(test_db, test_user):
    post = Post(
        user_id=test_user.id,
        title="Test Post",
        content="Test content",
        visibility=VisibilityType.PUBLIC
    )
    test_db.add(post)
    test_db.commit()
    test_db.refresh(post)
    return post

@pytest.fixture(scope="function")
def test_comment(test_db, test_user, test_post):
    comment = Comment(
        user_id=test_user.id,
        post_id=test_post.id,
        content="Test comment"
    )
    test_db.add(comment)
    test_db.commit()
    test_db.refresh(comment)
    return comment

@pytest.fixture(scope="function")
def test_nested_comment(test_db, test_user, test_post, test_comment):
    nested_comment = Comment(
        user_id=test_user.id,
        post_id=test_post.id,
        parent_id=test_comment.id,
        content="Nested test comment"
    )
    test_db.add(nested_comment)
    test_db.commit()
    test_db.refresh(nested_comment)
    return nested_comment