def test_reactivate_user(client):
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.get_json()["data"]["access_token"]

    create_resp = client.post(
        "/api/user/new",
        json={
            "name": "User to Reactivate",
            "email": "reactivateuser@test.com",
            "password": "123456"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert create_resp.status_code == 201
    data = create_resp.get_json()
    user_id = data.get("data", {}).get("user", {}).get("id")
    assert user_id is not None

    disable_resp = client.patch(
        f"/api/user/{user_id}/desactivate",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert disable_resp.status_code == 200

    reactivate_resp = client.patch(
        f"/api/user/{user_id}/reactivate",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert reactivate_resp.status_code == 200
    data = reactivate_resp.get_json()
    # Normalmente o campo ativo deve vir dentro de data -> user ou direto?
    active = data.get("data", {}).get("user", {}).get("active")
    assert active is True


def test_desactivate_user(client):
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.get_json()["data"]["access_token"]

    user_data = {
        "name": "User to Disable",
        "email": "disableuser@test.com",
        "password": "123456"
    }
    create_resp = client.post(
        "/api/user/new",
        json=user_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert create_resp.status_code == 201
    user_id = create_resp.get_json().get("data", {}).get("user", {}).get("id")
    assert user_id is not None

    disable_resp = client.patch(
        f"/api/user/{user_id}/desactivate",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert disable_resp.status_code == 200
    data = disable_resp.get_json()
    active = data.get("data", {}).get("user", {}).get("active")
    assert active is False


def test_update_user(client):
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.get_json()["data"]["access_token"]

    user_data = {
        "name": "User To Update",
        "email": "updateuser@test.com",
        "password": "123456"
    }
    create_resp = client.post(
        "/api/user/new",
        json=user_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert create_resp.status_code == 201
    user_id = create_resp.get_json().get("data", {}).get("user", {}).get("id")
    assert user_id is not None

    update_data = {
        "name": "User Updated",
        "email": "updateuser@test.com",
        "password": "123456",
        "role": "user",
        "active": True
    }
    update_resp = client.put(
        f"/api/user/{user_id}/update",
        json=update_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert update_resp.status_code == 200
    data = update_resp.get_json()
    user = data.get("data", {}).get("user")
    assert user is not None
    assert user["name"] == "User Updated"
    assert user["email"] == "updateuser@test.com"


def test_create_user(client):
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.get_json()["data"]["access_token"]

    user_data = {
        "name": "User Teste Novo",
        "email": "userteste_novo@test.com",
        "password": "123456"
    }
    resp = client.post(
        "/api/user/new",
        json=user_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 201
    data = resp.get_json()
    user = data.get("data", {}).get("user")
    assert user is not None
    assert user["email"] == "userteste_novo@test.com"


def test_list_users_actives(client):
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.get_json()["data"]["access_token"]

    resp = client.get(
        "/api/user/actives",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    users = data.get("data", {}).get("users", [])
    assert isinstance(users, list)
    assert any(user["email"] == "admin@email.com" for user in users)


def test_list_all_users(client):
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.get_json()["data"]["access_token"]

    resp = client.get(
        "/api/user/all",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    users = data.get("data", {}).get("users", [])
    assert isinstance(users, list)
    assert len(users) > 0
