import jwt
from config import Config

def test_register_sale(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # Decodifica o token 
    payload = jwt.decode(access_token, Config.SECRET_KEY, algorithms=["HS256"])
    user_id = payload["id"]

    # Para registrar uma venda, precisamos criar uma categoria, um produto e um cliente

    # Cria categoria
    cat_resp = client.post(
        "/api/category/new",
        json={"name": "VendaCat"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert cat_resp.status_code == 201
    cat_id = cat_resp.get_json()["category"]["id"]

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
    prod_id = prod_resp.get_json()["product"]["id"]

    # Cria cliente
    cli_resp = client.post(
        "/api/customer/new",
        json={"name": "Cliente Venda", "email": "clientevenda@test.com"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert cli_resp.status_code == 201
    cli_data = cli_resp.get_json()
    client_id = cli_data["customer"].get("id") if "customer" in cli_data else None
    assert client_id is not None

    # Registra a venda
    venda_resp = client.post(
        "/api/sale/register",
        json={
            "customer_id": client_id,
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
    assert "sale" in data

def test_list_sale(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    
    resp = client.get(
        "/api/sale/list",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "sales" in data
    assert isinstance(data["sales"], list)