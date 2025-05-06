import pytest
from fastapi.testclient import TestClient
import json

def test_get_users(client, test_user):
    """Test retrieving all users."""
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 1
    
    # Check that our test user is in the response
    found_test_user = False
    for user in users:
        if user["id"] == test_user.id:
            found_test_user = True
            assert user["username"] == test_user.username
            assert user["email"] == test_user.email
            assert "password_hash" not in user  # Ensure sensitive data is not returned
            break
    
    assert found_test_user

def test_get_user_by_id(client, test_user):
    """Test retrieving a specific user by ID."""
    response = client.get(f"/api/v1/users/{test_user.id}")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == test_user.id
    assert user["username"] == test_user.username
    assert user["email"] == test_user.email
    assert user["bio"] == test_user.bio
    assert "password_hash" not in user  # Ensure sensitive data is not returned

def test_get_nonexistent_user(client):
    """Test retrieving a user that doesn't exist."""
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_create_user(client):
    """Test creating a new user."""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "bio": "I am a new user",
        "profile_image_url": "http://example.com/image.jpg",
        "cover_image_url": "http://example.com/cover.jpg"
    }
    
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == 201
    
    created_user = response.json()
    assert created_user["username"] == user_data["username"]
    assert created_user["email"] == user_data["email"]
    assert created_user["bio"] == user_data["bio"]
    assert created_user["profile_image_url"] == user_data["profile_image_url"]
    assert created_user["cover_image_url"] == user_data["cover_image_url"]
    assert "password" not in created_user  # Password should not be returned
    assert "password_hash" not in created_user  # Hash should not be returned

def test_create_user_duplicate_username(client, test_user):
    """Test creating a user with a duplicate username."""
    user_data = {
        "username": test_user.username,  # Same username as test_user
        "email": "different@example.com",
        "password": "password123"
    }
    
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()

def test_create_user_duplicate_email(client, test_user):
    """Test creating a user with a duplicate email."""
    user_data = {
        "username": "differentuser",
        "email": test_user.email,  # Same email as test_user
        "password": "password123"
    }
    
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()

def test_update_user(client, test_user):
    """Test updating a user."""
    update_data = {
        "bio": "Updated bio",
        "profile_image_url": "http://example.com/new_image.jpg"
    }
    
    response = client.put(f"/api/v1/users/{test_user.id}", json=update_data)
    assert response.status_code == 200
    
    updated_user = response.json()
    assert updated_user["id"] == test_user.id
    assert updated_user["username"] == test_user.username  # Unchanged
    assert updated_user["email"] == test_user.email  # Unchanged
    assert updated_user["bio"] == update_data["bio"]  # Updated
    assert updated_user["profile_image_url"] == update_data["profile_image_url"]  # Updated

def test_update_nonexistent_user(client):
    """Test updating a user that doesn't exist."""
    update_data = {
        "bio": "Updated bio"
    }
    
    response = client.put("/api/v1/users/999", json=update_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_delete_user(client, test_db):
    """Test deleting a user."""
    # Create a user to delete
    from app.models.user import User
    temp_user = User(
        username="todelete",
        email="delete@example.com",
        password_hash="hashed_password"
    )
    test_db.add(temp_user)
    test_db.commit()
    test_db.refresh(temp_user)
    
    user_id = temp_user.id
    
    # Delete the user
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204
    
    # Verify the user is deleted
    check_response = client.get(f"/api/v1/users/{user_id}")
    assert check_response.status_code == 404

def test_delete_nonexistent_user(client):
    """Test deleting a user that doesn't exist."""
    response = client.delete("/api/v1/users/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_login_user(client, test_user):
    """Test updating the last_login time for a user."""
    response = client.post(f"/api/v1/users/{test_user.id}/login")
    assert response.status_code == 200
    
    logged_in_user = response.json()
    assert logged_in_user["id"] == test_user.id
    assert logged_in_user["last_login"] is not None  # Should be updated

def test_login_nonexistent_user(client):
    """Test logging in a user that doesn't exist."""
    response = client.post("/api/v1/users/999/login")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()