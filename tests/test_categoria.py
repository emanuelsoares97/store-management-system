

def test_listar_categorias(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # Cria uma categoria para garantir que haja ao menos uma na listagem
    create_resp = client.post(
        "/api/categoria/nova",
        json={"nome": "TestCategoria"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert create_resp.status_code == 201

    # Agora lista as categorias
    list_resp = client.get(
        "/api/categoria/lista",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert list_resp.status_code == 200
    data = list_resp.get_json()
    assert "categorias" in data
    # Verifica se a categoria recém-criada está presente
    assert any(cat.get("nome") == "TestCategoria" for cat in data["categorias"])

def test_atualizar_categoria(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # Cria uma categoria para atualizar
    create_resp = client.post(
        "/api/categoria/nova",
        json={"nome": "OldCategoria"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert create_resp.status_code == 201
    categoria_id = create_resp.get_json()["categoria"]["id"]

    # Atualiza a categoria
    update_resp = client.put(
        f"/api/categoria/{categoria_id}/editar",
        json={"nome": "UpdatedCategoria"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert update_resp.status_code == 200
    data = update_resp.get_json()
    assert "mensagem" in data
    assert "categoria" in data
    assert data["categoria"]["nome"] == "UpdatedCategoria"