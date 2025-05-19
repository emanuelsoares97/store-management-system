

def test_listar_categories(client):
    # Faz login para obter token válido
    login = client.post(
        "/api/auth/login", json={
            "email": "admin@email.com",
            "password": "123456"
        }
    )
    assert login.status_code == 200
    token = login.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Cria uma categoria para garantir listagem
    create_resp = client.post(
        "/api/category/new",
        json={"name": "TestCategory"},
        headers=headers
    )
    assert create_resp.status_code == 201

    # Lista categorias
    list_resp = client.get(
        "/api/category/list",
        headers=headers
    )
    assert list_resp.status_code == 200
    data = list_resp.get_json()

    # Verifica chave e conteúdo
    assert "categories" in data
    assert isinstance(data["categories"], list)
    assert any(cat["name"] == "TestCategory" for cat in data["categories"])


def test_update_category(client):
    # Faz login para obter token válido
    login = client.post(
        "/api/auth/login", json={
            "email": "admin@email.com",
            "password": "123456"
        }
    )
    assert login.status_code == 200
    token = login.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Cria categoria inicial
    create_resp = client.post(
        "/api/category/new",
        json={"name": "nome1"},
        headers=headers
    )
    assert create_resp.status_code == 201
    cat_id = create_resp.get_json()["category"]["id"]

    # Atualiza categoria
    update_resp = client.put(
        f"/api/category/{cat_id}/update",
        json={"name": "nome2"},
        headers=headers
    )
    assert update_resp.status_code == 200
    data = update_resp.get_json()

    # Verifica retorno
    assert "message" in data
    assert data["category"]["name"] == "nome2"

def test_criar_categoria_admin(client):
    """Teste para criar categoria"""

    # 1️⃣ Faz login e pega o token
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # 2️⃣ Envia requisição para criar a categoria usando o token correto
    response = client.post("/api/categoria/nova", json={"nome": "Fruta"}, headers={
        "Authorization": f"Bearer {access_token}"
    })

    # 3️⃣ Verifica se a categoria foi criada com sucesso
    assert response.status_code == 201
    assert "categoria" in response.json  # ✅ Agora verifica a chave correta
    assert "id" in response.json["categoria"]  # ✅ Verifica dentro de "categoria"
    assert response.json["categoria"]["nome"] == "Fruta"  # ✅ Confirma o nome correto
    assert response.json["mensagem"] == "Categoria criada com sucesso!"  # ✅ Confirma a mensagem
