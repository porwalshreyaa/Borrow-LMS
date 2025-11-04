def test_sql_injection(client):
    response = client.post("/api/users", json={
        "username": "injection",
        "email": "'; DROP TABLE user; --"
    })
    assert response.status_code in [400, 409]

def test_large_payload(client):
    big_email = "x" * 5000 + "@example.com"
    res = client.post("/api/users", json={
        "username": "bigboy",
        "email": big_email
    })
    assert res.status_code in [400, 413]
