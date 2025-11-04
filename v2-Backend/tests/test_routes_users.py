import json
from app.models.user import User
from app.extensions import db
def test_create_user(client):
    response = client.post("/api/users", json={
        "username": "alice",
        "email": "alice@example.com",
        "role": "student"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "alice"

def test_duplicate_email(client):
    client.post("/api/users", json={
        "username": "bob",
        "email": "bob@example.com"
    })
    response = client.post("/api/users", json={
        "username": "bobby",
        "email": "bob@example.com"
    })
    assert response.status_code == 409

def test_invalid_role(client):
    response = client.post("/api/users", json={
        "username": "charlie",
        "email": "charlie@example.com",
        "role": "hacker"
    })
    assert response.status_code == 400
