import jwt
from config import Config

def test_register_sale(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["data"]["access_token"]

    # Decodifica o token 
    payload = jwt.decode(access_token, Config.SECRET_KEY, algorithms=["HS256"])
    user_id = payload["id"]

    # Cria categoria
    cat_resp = client.post(
        "/api/category/new",
        json={"name": "VendaCat"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert cat_resp.status_code == 201
    cat_id = cat_resp.get_json()["data"]["category"]["id"]

    # Cria produto
    prod_resp = client.post(
        "/api/product/new",
        json={
            "name": "ProdutoVenda",
            "price": 10.0,
            "stock_quantity": 100,
            "category_id": cat_id
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert prod_resp.status_code == 201
    prod_id = prod_resp.get_json()["data"]["product"]["id"]

    # Prepara dados do cliente (não precisa criar porque o serviço cria/acha)
    customer_data = {
        "name": "Cliente Venda",
        "email": "clientevenda@test.com"
    }

    # Registra a venda, enviando o cliente aninhado
    venda_resp = client.post(
        "/api/sale/register",
        json={
            "customer": customer_data,
            "user_id": user_id,
            "product_id": prod_id,
            "quantity": 2
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert venda_resp.status_code == 201
    data = venda_resp.get_json()
    assert "message" in data
    assert data["message"] == "Venda registrada com sucesso!"
    assert "sale" in data["data"]


def test_list_sale(client):
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["data"]["access_token"]

    resp = client.get(
        "/api/sale/list",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()

    assert "data" in data
    assert "sales" in data["data"]
    assert isinstance(data["data"]["sales"], list)
