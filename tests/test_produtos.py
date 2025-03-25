

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


def test_criar_produto_admin(client):
    """Testa se o admin consegue criar um produto"""
    # 1Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # 2Cria uma categoria de teste para o produto
    response_categoria = client.post(
        "/api/categoria/nova", 
        json={"nome": "Categoria Teste"}, 
        headers={"Authorization": f"Bearer {access_token}"}
    )
    # Se a categoria já existir, adapte conforme o retorno da API
    assert response_categoria.status_code == 201

    categoria_id = response_categoria.json["categoria"]["id"]

    # Define os dados do produto, usando a categoria recém-criada
    produto_data = {
        "nome": "banana",
        "preco": 3.0,
        "quantidade_estoque": 10,
        "categoria_id": categoria_id
    }

    # Envia a requisição POST para criar o produto
    response_produto = client.post(
        "/api/produto/novo",
        json=produto_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    # Verifica a resposta
    assert response_produto.status_code == 201, "Deveria retornar 201 Created"
    data = response_produto.get_json()
    assert "produto" in data, "Resposta deve conter a chave 'produto'"
    produto = data["produto"]
    assert produto["nome"] == "banana", "O nome do produto deve ser 'banana'"
    assert produto["preco"] == 3.0, "O preço do produto deve ser 3.0"
    assert produto["quantidade_estoque"] == 10, "A quantidade em estoque deve ser 10"


def test_validar_lista_de_produtos(client):
    """Testa se uma rota protegida retorna 200 com token válido"""

    # faz o login e pega o token
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # entra numa rota get e usa o token para ter autorizaçao de acesso a rota
    response = client.get("/api/produto/ativos", headers={"Authorization": f"Bearer {access_token}"})

    # Valida se a resposta foi bem-sucedida
    assert response.status_code == 200
    assert "produtos" in response.json  # Garante que a chave 'produtos' existe na resposta.
    assert isinstance(response.json["produtos"], list)  # Agora verificamos corretamente a lista.