from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_get_token():
    response = client.post(
        "/token",
        data={"username": "user1", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_user():
    response = client.post(
        "/users/",
        json={"username": "newuser", "email": "newuser@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"

def test_invalid_token():
    response = client.get("/protected-endpoint", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}
