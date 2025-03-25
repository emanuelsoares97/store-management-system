def test_listar_clientes(client):
    token, _ = get_token(client)
    # Cria um cliente para garantir que haja ao menos um
    create_resp = client.post(
        "/api/cliente/novo",
        json={"nome": "Cliente Teste", "email": "cliente1@test.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_resp.status_code == 201

    # Lista os clientes
    list_resp = client.get(
        "/api/cliente/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert list_resp.status_code == 200
    data = list_resp.get_json()
    assert "clientes" in data
    assert any(cli.get("email") == "cliente1@test.com" for cli in data["clientes"])

def test_criar_cliente(client):
    token, _ = get_token(client)
    resp = client.post(
        "/api/cliente/novo",
        json={"nome": "Cliente Novo", "email": "cliente2@test.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert "mensagem" in data
    assert data["mensagem"] == "Cliente criado com sucesso!"
    assert "cliente" in data
    assert data["cliente"]["email"] == "cliente2@test.com"