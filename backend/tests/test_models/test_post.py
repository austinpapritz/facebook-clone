import pytest
from datetime import datetime, timedelta
from sqlalchemy import update
from app.models.post import Post, VisibilityType

def test_create_post(test_db, test_user):
    """Test post creation with all fields."""
    post = Post(
        user_id=test_user.id,
        title="Test Title",
        content="Test content for the post",
        image_url="http://example.com/image.jpg",
        visibility=VisibilityType.PUBLIC
    )
    test_db.add(post)
    test_db.commit()
    test_db.refresh(post)

    assert post.id is not None
    assert post.user_id == test_user.id
    assert post.title == "Test Title"
    assert post.content == "Test content for the post"
    assert post.image_url == "http://example.com/image.jpg"
    assert post.visibility == VisibilityType.PUBLIC
    assert post.created_at is not None
    assert post.updated_at is not None

def test_create_minimal_post(test_db, test_user):
    """Test post creation with only required fields."""
    post = Post(
        user_id=test_user.id,
        content="Minimal post content"
    )
    test_db.add(post)
    test_db.commit()
    test_db.refresh(post)

    assert post.id is not None
    assert post.user_id == test_user.id
    assert post.title is None
    assert post.content == "Minimal post content"
    assert post.image_url is None
    assert post.visibility == VisibilityType.PUBLIC  # Default value
    assert post.created_at is not None
    assert post.updated_at is not None

def test_post_user_relationship(test_db, test_post):
    """Test the relationship between posts and users."""
    post = test_db.query(Post).filter(Post.id == test_post.id).first()
    
    assert post.user is not None
    assert post.user.id == test_post.user_id
    assert post.user.username == "testuser"  # From the test_user fixture

def test_post_visibility_enum(test_db, test_user):
    """Test the visibility enum values."""
    # Create posts with different visibility settings
    public_post = Post(user_id=test_user.id, content="Public post", visibility=VisibilityType.PUBLIC)
    friends_post = Post(user_id=test_user.id, content="Friends post", visibility=VisibilityType.FRIENDS)
    private_post = Post(user_id=test_user.id, content="Private post", visibility=VisibilityType.PRIVATE)
    
    test_db.add_all([public_post, friends_post, private_post])
    test_db.commit()
    
    # Retrieve posts
    posts = test_db.query(Post).filter(Post.user_id == test_user.id).order_by(Post.id).all()
    
    assert len(posts) >= 3
    # Check only the ones we just added to avoid issues with other fixtures
    found_public = False
    found_friends = False
    found_private = False
    
    for post in posts:
        if post.content == "Public post":
            assert post.visibility == VisibilityType.PUBLIC
            found_public = True
        elif post.content == "Friends post":
            assert post.visibility == VisibilityType.FRIENDS
            found_friends = True
        elif post.content == "Private post":
            assert post.visibility == VisibilityType.PRIVATE
            found_private = True
    
    assert found_public
    assert found_friends
    assert found_private

def test_update_post_timestamp(test_db, test_post):
    """Test that updated_at timestamp changes on update."""
    # Get the original timestamp
    original_timestamp = test_post.updated_at
    
    # Wait a moment to ensure the timestamp will be different
    import time
    time.sleep(0.1)
    
    # Update the post
    stmt = update(Post).where(Post.id == test_post.id).values(content="Updated content")
    test_db.execute(stmt)
    test_db.commit()
    
    # Refresh the post
    test_db.refresh(test_post)
    
    # Check that the timestamp has changed
    assert test_post.updated_at > original_timestamp
    assert test_post.content == "Updated content"