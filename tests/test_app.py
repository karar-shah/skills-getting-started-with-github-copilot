import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities

def test_get_activities():
    # Arrange
    # (No setup needed, just use the client)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("description" in v for v in data.values())

# Test POST /activities/{activity}/signup

def test_signup_success():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert "message" in response.json()

# Test duplicate signup

def test_signup_duplicate():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "dupeuser@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "detail" in response.json()

# Test DELETE /activities/{activity}/signup

def test_unregister_success():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "removeuser@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert "message" in response.json()

# Test unregister non-existent participant

def test_unregister_nonexistent():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "notfound@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "detail" in response.json()
