import pytest
from fastapi.testclient import TestClient
from app.models.post import VisibilityType

def test_get_posts(client, test_post):
    """Test retrieving all posts."""
    response = client.get("/api/v1/posts")
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) >= 1
    
    # Check that our test post is in the response
    found_test_post = False
    for post in posts:
        if post["id"] == test_post.id:
            found_test_post = True
            assert post["user_id"] == test_post.user_id
            assert post["content"] == test_post.content
            break
    
    assert found_test_post

def test_get_post_by_id(client, test_post, test_user):
    """Test retrieving a specific post by ID."""
    response = client.get(f"/api/v1/posts/{test_post.id}")
    assert response.status_code == 200
    post = response.json()
    assert post["id"] == test_post.id
    assert post["user_id"] == test_post.user_id
    assert post["content"] == test_post.content
    
    # Check that user information is included
    assert "user" in post
    assert post["user"]["id"] == test_user.id
    assert post["user"]["username"] == test_user.username

def test_get_nonexistent_post(client):
    """Test retrieving a post that doesn't exist."""
    response = client.get("/api/v1/posts/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_create_post(client, test_user):
    """Test creating a new post."""
    post_data = {
        "title": "New Post Title",
        "content": "This is the content of the new post",
        "image_url": "http://example.com/image.jpg",
        "visibility": "public"
    }
    
    response = client.post(f"/api/v1/posts?user_id={test_user.id}", json=post_data)
    assert response.status_code == 201
    
    created_post = response.json()
    assert created_post["title"] == post_data["title"]
    assert created_post["content"] == post_data["content"]
    assert created_post["image_url"] == post_data["image_url"]
    assert created_post["visibility"] == post_data["visibility"]
    assert created_post["user_id"] == test_user.id

def test_create_minimal_post(client, test_user):
    """Test creating a post with only required fields."""
    post_data = {
        "content": "This is a minimal post"
    }
    
    response = client.post(f"/api/v1/posts?user_id={test_user.id}", json=post_data)
    assert response.status_code == 201
    
    created_post = response.json()
    assert created_post["content"] == post_data["content"]
    assert created_post["title"] is None
    assert created_post["image_url"] is None
    assert created_post["visibility"] == "public"  # Default value
    assert created_post["user_id"] == test_user.id

def test_update_post(client, test_post):
    """Test updating a post."""
    update_data = {
        "title": "Updated Title",
        "content": "Updated content"
    }
    
    response = client.put(f"/api/v1/posts/{test_post.id}", json=update_data)
    assert response.status_code == 200
    
    updated_post = response.json()
    assert updated_post["id"] == test_post.id
    assert updated_post["title"] == update_data["title"]
    assert updated_post["content"] == update_data["content"]
    # Other fields should remain unchanged
    assert updated_post["user_id"] == test_post.user_id

def test_update_post_visibility(client, test_post):
    """Test updating only the visibility of a post."""
    update_data = {
        "visibility": "private"
    }
    
    response = client.put(f"/api/v1/posts/{test_post.id}", json=update_data)
    assert response.status_code == 200
    
    updated_post = response.json()
    assert updated_post["id"] == test_post.id
    assert updated_post["visibility"] == "private"
    # Other fields should remain unchanged
    assert updated_post["content"] == test_post.content

def test_update_nonexistent_post(client):
    """Test updating a post that doesn't exist."""
    update_data = {
        "title": "Updated Title"
    }
    
    response = client.put("/api/v1/posts/999", json=update_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_delete_post(client, test_db):
    """Test deleting a post."""
    # Create a post to delete
    from app.models.post import Post
    temp_post = Post(
        user_id=1,  # Assuming test_user has ID 1
        content="Post to delete"
    )
    test_db.add(temp_post)
    test_db.commit()
    test_db.refresh(temp_post)
    
    post_id = temp_post.id
    
    # Delete the post
    response = client.delete(f"/api/v1/posts/{post_id}")
    assert response.status_code == 204
    
    # Verify the post is deleted
    check_response = client.get(f"/api/v1/posts/{post_id}")
    assert check_response.status_code == 404

def test_delete_nonexistent_post(client):
    """Test deleting a post that doesn't exist."""
    response = client.delete("/api/v1/posts/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_get_user_posts(client, test_user, test_post):
    """Test retrieving all posts by a specific user."""
    response = client.get(f"/api/v1/users/{test_user.id}/posts")
    assert response.status_code == 200
    
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) >= 1
    
    # Check that our test post is in the response
    found_test_post = False
    for post in posts:
        if post["id"] == test_post.id:
            found_test_post = True
            assert post["user_id"] == test_user.id
            assert post["content"] == test_post.content
            break
    
    assert found_test_post