def test_reativar_utilizador(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # Cria um utilizador para reativar
    user_data = {
        "nome": "User to Reactivate",
        "email": "reactivateuser@test.com",
        "password": "123456"
    }
    create_resp = client.post(
        "/api/utilizador/novo",
        json=user_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert create_resp.status_code in (200, 201)
    user_id = create_resp.get_json().get("id") or create_resp.get_json().get("utilizador", {}).get("id")
    assert user_id is not None

    # Desativa o utilizador
    disable_resp = client.patch(
        f"/api/utilizador/{user_id}/desativar",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert disable_resp.status_code == 200

    # Reativa o utilizador
    reactivate_resp = client.patch(
        f"/api/utilizador/{user_id}/reativar",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert reactivate_resp.status_code == 200
    data = reactivate_resp.get_json()
    if "ativo" in data:
        assert data["ativo"] is True

def test_desativar_utilizador(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # Cria um utilizador para desativar
    user_data = {
        "nome": "User to Disable",
        "email": "disableuser@test.com",
        "password": "123456"
    }
    create_resp = client.post(
        "/api/utilizador/novo",
        json=user_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert create_resp.status_code in (200, 201)
    user_id = create_resp.get_json().get("id") or create_resp.get_json().get("utilizador", {}).get("id")
    assert user_id is not None

    # Desativa o utilizador
    disable_resp = client.patch(
        f"/api/utilizador/{user_id}/desativar",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert disable_resp.status_code == 200
    data = disable_resp.get_json()
    # Se a resposta retornar o campo 'ativo', deve ser False
    if "ativo" in data:
        assert data["ativo"] is False


def test_atualizar_utilizador(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # Cria um utilizador para atualizar
    user_data = {
        "nome": "User To Update",
        "email": "updateuser@test.com",
        "password": "123456"
    }
    create_resp = client.post(
        "/api/utilizador/novo",
        json=user_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert create_resp.status_code in (200, 201)
    # Obtém o ID do novo utilizador
    user_id = create_resp.get_json().get("id") or create_resp.get_json().get("utilizador", {}).get("id")
    assert user_id is not None

    # Atualiza os dados do utilizador
    update_data = {
        "nome": "User Updated",
        "email": "updateuser@test.com",
        "password": "123456",
        "role": "user",
        "ativo": True
    }
    update_resp = client.put(
        f"/api/utilizador/{user_id}/editar",
        json=update_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert update_resp.status_code == 200
    data = update_resp.get_json()
    assert "nome" in data and data["nome"] == "User Updated"

def test_criar_utilizador(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # Dados do novo utilizador; use um email único se necessário
    user_data = {
        "nome": "User Teste Novo",
        "email": "userteste_novo@test.com",
        "password": "123456"
    }
    resp = client.post(
        "/api/utilizador/novo",
        json=user_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code in (200, 201)
    data = resp.get_json()
    # Verifica se o email do utilizador criado corresponde
    if "utilizador" in data:
        assert data["utilizador"]["email"] == "userteste_novo@test.com"
    else:
        assert data.get("email") == "userteste_novo@test.com"

def test_listar_utilizadores_ativos(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    resp = client.get(
        "/api/utilizador/ativos",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    # A resposta deve ser uma lista de utilizadores ativos
    assert isinstance(data, list)
    # Verifica se o admin está na lista
    assert any(u.get("email") == "admin@email.com" for u in data)

def test_listar_todos_utilizadores(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    resp = client.get(
        "/api/utilizador/todos",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) > 0