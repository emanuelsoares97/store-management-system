def test_list_categories(client):
    # Faz login para obter token válido
    login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert login.status_code == 200
    token = login.get_json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Cria uma categoria
    create_resp = client.post("/api/category/new", json={"name": "TestCategory"}, headers=headers)
    assert create_resp.status_code == 201

    # Lista categorias
    list_resp = client.get("/api/category/list", headers=headers)
    assert list_resp.status_code == 200
    data = list_resp.get_json()

    assert "data" in data
    assert "categories" in data["data"]
    assert isinstance(data["data"]["categories"], list)
    assert any(cat["name"] == "TestCategory" for cat in data["data"]["categories"])

def test_update_category(client):
    # Faz login para obter token válido
    login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert login.status_code == 200
    token = login.get_json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Cria categoria inicial
    create_resp = client.post("/api/category/new", json={"name": "nome1"}, headers=headers)
    assert create_resp.status_code == 201
    cat_id = create_resp.get_json()["data"]["category"]["id"]

    # Atualiza categoria
    update_resp = client.put(f"/api/category/{cat_id}/update", json={"name": "nome2"}, headers=headers)
    assert update_resp.status_code == 200
    data = update_resp.get_json()

    assert "message" in data
    assert data["data"]["category"]["name"] == "nome2"

def test_create_new_category(client):
    """Teste para criar categoria"""
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.get_json()["data"]["access_token"]

    response = client.post("/api/category/new", json={"name": "Fruta"}, headers={
        "Authorization": f"Bearer {access_token}"
    })

    assert response.status_code == 201
    data = response.get_json()

    assert "data" in data
    assert "category" in data["data"]
    assert "id" in data["data"]["category"]
    assert data["data"]["category"]["name"] == "Fruta"
    assert data["message"] == "Categoria criada com sucesso!"
