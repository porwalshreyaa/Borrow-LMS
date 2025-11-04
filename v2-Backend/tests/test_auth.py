def test_login_invalid_credentials(client):
    response = client.post("/api/login", json={
        "email": "wrong@example.com",
        "password": "123"
    })
    assert response.status_code == 401
