import pytest
from app.db.init_db import seed_data
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
import time

def test_seed_data(test_db):
    """Test that the seed_data function properly populates the database."""
    # Run the seed function
    seed_data(test_db)
    
    # Check that users were created
    users = test_db.query(User).all()
    assert len(users) >= 5  # The function creates 5 users
    
    # Check that posts were created
    posts = test_db.query(Post).all()
    assert len(posts) >= 10  # The function creates 2 posts per user
    
    # Check that comments were created
    comments = test_db.query(Comment).all()
    assert len(comments) >= 30  # The function creates 3 comments per post
    
    # Verify relationships
    for user in users:
        # Each user should have posts
        assert len(user.posts) > 0
        
    for post in posts:
        # Each post should have comments
        assert len(post.comments) > 0
        # Each post should have a user
        assert post.user is not None
        
    for comment in comments:
        # Each comment should have a user
        assert comment.user is not None
        # Each comment should have a post
        assert comment.post is not None

def test_init_db_idempotent(test_db, monkeypatch):
    """Test that running seed_data multiple times doesn't cause errors."""
    # Mock the faker to ensure predictable but unique usernames
    from faker import Faker
    import random
    
    # Use timestamps to ensure uniqueness
    timestamp1 = int(time.time() * 1000)
    timestamp2 = timestamp1 + 1000  # Ensure different timestamps
    
    class MockFaker:
        def __init__(self):
            self.counter = 0
            self.timestamp = timestamp1
            
        def user_name(self):
            self.counter += 1
            return f"testuser{self.counter}_{self.timestamp}_{random.randint(1000, 9999)}"
            
        def email(self):
            return f"test{self.counter}_{self.timestamp}@example.com"
            
        def password(self, length=12):
            return "password123"
            
        def paragraph(self):
            return "This is a test paragraph."
            
        def sentence(self):
            return "This is a test sentence."
    
    # First run with timestamp1
    monkeypatch.setattr("app.db.init_db.Faker", lambda: MockFaker())
    
    # Run seed_data once
    seed_data(test_db)
    first_count = test_db.query(User).count()
    
    # Update the timestamp for the second run
    class MockFaker2(MockFaker):
        def __init__(self):
            super().__init__()
            self.timestamp = timestamp2
    
    # Second run with timestamp2
    monkeypatch.setattr("app.db.init_db.Faker", lambda: MockFaker2())
    
    # Run it again with different timestamps in the usernames
    seed_data(test_db)
    second_count = test_db.query(User).count()
    
    # Count should increase by exactly 5 (the number of users created in seed_data)
    assert second_count == first_count + 5