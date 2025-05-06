import pytest
from sqlalchemy.exc import IntegrityError
from app.models.user import User

def test_create_user(test_db):
    """Test user creation with all fields."""
    user = User(
        username="newuser",
        email="new@example.com",
        password_hash="hashed_password",
        bio="User bio",
        profile_image_url="http://example.com/image.jpg",
        cover_image_url="http://example.com/cover.jpg",
        is_active=True,
        role="user"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    assert user.id is not None
    assert user.username == "newuser"
    assert user.email == "new@example.com"
    assert user.password_hash == "hashed_password"
    assert user.bio == "User bio"
    assert user.profile_image_url == "http://example.com/image.jpg"
    assert user.cover_image_url == "http://example.com/cover.jpg"
    assert user.is_active is True
    assert user.role == "user"
    assert user.created_at is not None
    assert user.updated_at is not None

def test_create_minimal_user(test_db):
    """Test user creation with only required fields."""
    user = User(
        username="minimaluser",
        email="minimal@example.com",
        password_hash="hashed_password"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    assert user.id is not None
    assert user.username == "minimaluser"
    assert user.email == "minimal@example.com"
    assert user.password_hash == "hashed_password"
    assert user.bio is None
    assert user.profile_image_url is None
    assert user.cover_image_url is None
    assert user.is_active is True  # Default value
    assert user.role == "user"  # Default value
    assert user.created_at is not None
    assert user.updated_at is not None

def test_unique_username_constraint(test_db, test_user):
    """Test that username must be unique."""
    duplicate_user = User(
        username=test_user.username,  # Same username as test_user
        email="different@example.com",
        password_hash="hashed_password"
    )
    test_db.add(duplicate_user)
    
    with pytest.raises(IntegrityError):
        test_db.commit()
    
    test_db.rollback()

def test_unique_email_constraint(test_db, test_user):
    """Test that email must be unique."""
    duplicate_user = User(
        username="differentuser",
        email=test_user.email,  # Same email as test_user
        password_hash="hashed_password"
    )
    test_db.add(duplicate_user)
    
    with pytest.raises(IntegrityError):
        test_db.commit()
    
    test_db.rollback()

def test_user_posts_relationship(test_db, test_user, test_post):
    """Test the relationship between users and posts."""
    user = test_db.query(User).filter(User.id == test_user.id).first()
    
    assert len(user.posts) == 1
    assert user.posts[0].id == test_post.id
    assert user.posts[0].content == test_post.content