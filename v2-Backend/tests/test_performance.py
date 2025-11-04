import time

def test_create_user_performance(client):
    start = time.time()
    for i in range(50):
        client.post("/api/users", json={
            "username": f"user{i}",
            "email": f"user{i}@example.com"
        })
    duration = time.time() - start
    assert duration < 1.5  