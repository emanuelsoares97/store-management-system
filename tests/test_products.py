def test_create_product_admin(client):
    """Testa se o admin consegue criar um produto"""
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # Cria uma categoria de teste para o produto
    response_cat= client.post(
        "/api/category/new", 
        json={"name": "Categoria Teste"}, 
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response_cat.status_code == 201

    categoria_id = response_cat.json["category"]["id"]

    # Envia a requisição POST para criar o produto
    resp = client.post(
        "/api/product/new",
        json={
        "name": "banana",
        "price": 3.0,
        "stock_quantity": 10,
        "category_id": categoria_id
    },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    # Verifica a resposta
    assert resp.status_code == 201
    data = resp.get_json()
    assert "product" in data
    product = data["product"]
    assert product["name"] == "banana"
    assert product["price"] == 3.0
    assert product["stock_quantity"] == 10


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