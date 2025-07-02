def test_create_product_admin(client):
    """Testa se o admin consegue criar um produto"""
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["data"]["access_token"]

    # Cria uma categoria de teste para o produto
    response_cat= client.post(
        "/api/category/new", 
        json={"name": "Categoria Teste"}, 
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response_cat.status_code == 201

    categoria_id = response_cat.json["data"]["category"]["id"]

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
    assert "product" in data["data"]
    product = data["data"]["product"]
    assert product["name"] == "banana"
    assert product["price"] == 3.0
    assert product["stock_quantity"] == 10


def test_validate_list_products(client):
    """Testa se uma rota protegida retorna 200 com token válido"""

        # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["data"]["access_token"]

    # entra numa rota get e usa o token para ter autorizaçao de acesso a rota
    response = client.get("/api/product/active", 
                headers={"Authorization": f"Bearer {access_token}"})

    # Valida se a resposta foi bem-sucedida

    data = response.get_json()

    assert response.status_code == 200
    assert "products" in data["data"]