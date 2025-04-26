def test_create_user(db_session):
    """Test basic user creation and retrieval."""
    from app.models.user import User
    from datetime import datetime
    
    # Create a test user
    test_user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password",
        last_login=datetime.now(),
        is_active=True,
        role="user"
    )
    
    db_session.add(test_user)
    db_session.commit()
    
    # Query the user
    queried_user = db_session.query(User).filter(User.username == "testuser").first()
    
    # Assertions
    assert queried_user is not None
    assert queried_user.email == "test@example.com"
    assert queried_user.is_active is True
    assert queried_user.role == "user"