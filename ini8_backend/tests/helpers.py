def get_auth_token(client):
    resp = client.post("/login", json={"username": "admin", "password": "admin"})
    assert resp.status_code == 200
    return resp.get_json()["token"]
