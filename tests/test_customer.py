def test_list_customer(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["data"]["access_token"]

    # Cria um cliente para garantir que haja ao menos um
    create_resp = client.post(
        "/api/customer/new",
        json={"name": "Cliente Teste", "email": "cliente1@test.com"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert create_resp.status_code == 201

    # Lista os clientes
    list_resp = client.get(
        "/api/customer/active",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert list_resp.status_code == 200
    data = list_resp.get_json()
    assert "customers" in data["data"]
    assert any(cli.get("email") == "cliente1@test.com" for cli in data["data"]["customers"])

def test_create_customer(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["data"]["access_token"]

    resp = client.post(
        "/api/customer/new",
        json={"name": "Cliente Novo", "email": "cliente2@test.com"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert "message" in data
    assert data["message"] == "Cliente criado com sucesso!"
    assert "customer" in data["data"]
    assert data["data"]["customer"]["email"] == "cliente2@test.com"