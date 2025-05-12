def test_get_comments(client, test_comment):
    """Test retrieving all comments."""
    response = client.get("/api/v1/comments")
    assert response.status_code == 200
    comments = response.json()
    assert isinstance(comments, list)
    assert len(comments) >= 1
    
    # Check that our test comment is in the response
    found_test_comment = False
    for comment in comments:
        if comment["id"] == test_comment.id:
            found_test_comment = True
            assert comment["user_id"] == test_comment.user_id
            assert comment["post_id"] == test_comment.post_id
            assert comment["content"] == test_comment.content
            break
    
    assert found_test_comment

def test_get_comment_by_id(client, test_comment, test_user):
    """Test retrieving a specific comment by ID."""
    response = client.get(f"/api/v1/comments/{test_comment.id}")
    assert response.status_code == 200
    comment = response.json()
    assert comment["id"] == test_comment.id
    assert comment["user_id"] == test_comment.user_id
    assert comment["post_id"] == test_comment.post_id
    assert comment["content"] == test_comment.content
    
    # Check that user information is included
    assert "user" in comment
    assert comment["user"]["id"] == test_user.id
    assert comment["user"]["username"] == test_user.username

def test_get_nonexistent_comment(client):
    """Test retrieving a comment that doesn't exist."""
    response = client.get("/api/v1/comments/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_create_comment(client, test_user, test_post):
    """Test creating a new comment."""
    comment_data = {
        "content": "This is a new comment",
        "post_id": test_post.id,
        "parent_id": None
    }
    
    response = client.post(f"/api/v1/comments?user_id={test_user.id}", json=comment_data)
    assert response.status_code == 201
    
    created_comment = response.json()
    assert created_comment["content"] == comment_data["content"]
    assert created_comment["post_id"] == comment_data["post_id"]
    assert created_comment["parent_id"] == comment_data["parent_id"]
    assert created_comment["user_id"] == test_user.id

def test_create_reply_comment(client, test_user, test_post, test_comment):
    """Test creating a reply to an existing comment."""
    comment_data = {
        "content": "This is a reply to another comment",
        "post_id": test_post.id,
        "parent_id": test_comment.id
    }
    
    response = client.post(f"/api/v1/comments?user_id={test_user.id}", json=comment_data)
    assert response.status_code == 201
    
    created_comment = response.json()
    assert created_comment["content"] == comment_data["content"]
    assert created_comment["post_id"] == comment_data["post_id"]
    assert created_comment["parent_id"] == comment_data["parent_id"]
    assert created_comment["user_id"] == test_user.id

def test_update_comment(client, test_comment):
    """Test updating a comment."""
    update_data = {
        "content": "Updated comment content"
    }
    
    response = client.put(f"/api/v1/comments/{test_comment.id}", json=update_data)
    assert response.status_code == 200
    
    updated_comment = response.json()
    assert updated_comment["id"] == test_comment.id
    assert updated_comment["content"] == update_data["content"]
    # Other fields should remain unchanged
    assert updated_comment["user_id"] == test_comment.user_id
    assert updated_comment["post_id"] == test_comment.post_id

def test_update_nonexistent_comment(client):
    """Test updating a comment that doesn't exist."""
    update_data = {
        "content": "Updated content"
    }
    
    response = client.put("/api/v1/comments/999", json=update_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_delete_comment(client, test_db, test_user, test_post):
    """Test deleting a comment."""
    # Create a comment to delete
    from app.models.comment import Comment
    temp_comment = Comment(
        user_id=test_user.id,
        post_id=test_post.id,
        content="Comment to delete"
    )
    test_db.add(temp_comment)
    test_db.commit()
    test_db.refresh(temp_comment)
    
    comment_id = temp_comment.id
    
    # Delete the comment
    response = client.delete(f"/api/v1/comments/{comment_id}")
    assert response.status_code == 204
    
    # Verify the comment is deleted
    check_response = client.get(f"/api/v1/comments/{comment_id}")
    assert check_response.status_code == 404

def test_delete_nonexistent_comment(client):
    """Test deleting a comment that doesn't exist."""
    response = client.delete("/api/v1/comments/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_get_post_comments(client, test_post, test_comment):
    """Test retrieving all comments for a specific post."""
    response = client.get(f"/api/v1/posts/{test_post.id}/comments")
    assert response.status_code == 200
    
    comments = response.json()
    assert isinstance(comments, list)
    
    # Check if test_comment is a top-level comment and included in the response
    if test_comment.parent_id is None:
        found_test_comment = False
        for comment in comments:
            if comment["id"] == test_comment.id:
                found_test_comment = True
                assert comment["post_id"] == test_post.id
                assert comment["content"] == test_comment.content
                break
        
        assert found_test_comment

def test_get_comment_replies(client, test_comment, test_nested_comment):
    """Test retrieving all replies to a specific comment."""
    response = client.get(f"/api/v1/comments/{test_comment.id}/replies")
    assert response.status_code == 200
    
    replies = response.json()
    assert isinstance(replies, list)
    assert len(replies) >= 1
    
    # Check that our test nested comment is in the response
    found_nested_comment = False
    for reply in replies:
        if reply["id"] == test_nested_comment.id:
            found_nested_comment = True
            assert reply["parent_id"] == test_comment.id
            assert reply["content"] == test_nested_comment.content
            break
    
    assert found_nested_comment