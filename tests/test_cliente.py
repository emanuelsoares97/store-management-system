def test_listar_clientes(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # Cria um cliente para garantir que haja ao menos um
    create_resp = client.post(
        "/api/cliente/novo",
        json={"nome": "Cliente Teste", "email": "cliente1@test.com"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert create_resp.status_code == 201

    # Lista os clientes
    list_resp = client.get(
        "/api/cliente/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert list_resp.status_code == 200
    data = list_resp.get_json()
    assert "clientes" in data
    assert any(cli.get("email") == "cliente1@test.com" for cli in data["clientes"])

def test_criar_cliente(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    resp = client.post(
        "/api/cliente/novo",
        json={"nome": "Cliente Novo", "email": "cliente2@test.com"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert "mensagem" in data
    assert data["mensagem"] == "Cliente criado com sucesso!"
    assert "cliente" in data
    assert data["cliente"]["email"] == "cliente2@test.com"