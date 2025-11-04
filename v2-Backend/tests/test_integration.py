def test_user_lifecycle(client):

    res = client.post("/api/users", json={
        "username": "eve",
        "email": "eve@example.com"
    })
    assert res.status_code == 201

    # fetch
    res = client.get("/api/users")
    users = res.get_json()
    assert any(u["email"] == "eve@example.com" for u in users)
