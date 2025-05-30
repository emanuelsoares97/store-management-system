def test_reactivate_user(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

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
    user_id = create_resp.get_json().get("id") or create_resp.get_json().get("user", {}).get("id")
    assert user_id is not None

    # Desativa o user
    disable_resp = client.patch(
        f"/api/user/{user_id}/desactivate",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert disable_resp.status_code == 200

    # Reativa o user
    reactivate_resp = client.patch(
        f"/api/user/{user_id}/reactivate",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert reactivate_resp.status_code == 200
    data = reactivate_resp.get_json()
    if "active" in data:
        assert data["active"] is True

def test_desactivate_user(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # Cria um user para desativar
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
    user_id = create_resp.get_json().get("id") or create_resp.get_json().get("user", {}).get("id")
    assert user_id is not None

    # Desativa o user
    disable_resp = client.patch(
        f"/api/user/{user_id}/desactivate",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert disable_resp.status_code == 200
    data = disable_resp.get_json()
    # Se a resposta retornar o campo 'active', deve ser False
    if "active" in data:
        assert data["active"] is False

def test_update_user(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # Cria um user para atualizar
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
    # Obtém o ID do novo user
    user_id = create_resp.get_json().get("id") or create_resp.get_json().get("user", {}).get("id")
    assert user_id is not None

    # Atualiza os dados do user
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
    user = data["user"]
    assert user["name"] == "User Updated"
    assert user["email"] == "updateuser@test.com"

def test_create_user(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # Dados do novo user; use um email único se necessário
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
    # Verifica se o email do user criado corresponde
    if "user" in data:
        assert data["user"]["email"] == "userteste_novo@test.com"
    else:
        assert data.get("email") == "userteste_novo@test.com"

def test_list_users_actives(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    resp = client.get(
        "/api/user/actives",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    users = data.get("users", [])
    assert isinstance(users, list)
    assert any(user["email"] == "admin@email.com" for user in users)

def test_list_all_users(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    resp = client.get(
        "/api/user/all",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert isinstance(data["users"], list)
    