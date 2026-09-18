def test_register_and_me(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "Grace", "email": "grace@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    token = response.get_json()["data"]["access_token"]
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.get_json()["data"]["email"] == "grace@example.com"


def test_login_rejects_bad_password(client):
    response = client.post("/api/auth/login", json={"email": "ada@example.com", "password": "wrongpass"})
    assert response.status_code == 401


def test_admin_stats_forbidden_for_user(client, auth_header):
    headers = auth_header
    response = client.get("/api/admin/stats", headers=headers)
    assert response.status_code == 403


def test_admin_stats_ok(client):
    login = client.post("/api/auth/login", json={"email": "admin@example.com", "password": "password123"})
    token = login.get_json()["data"]["access_token"]
    response = client.get("/api/admin/stats", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.get_json()["data"]["job_roles"] >= 1
