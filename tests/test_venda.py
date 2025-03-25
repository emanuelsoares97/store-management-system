import jwt
from config import Config

def test_registrar_venda(client):
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
        "/api/categoria/nova",
        json={"nome": "VendaCat"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert cat_resp.status_code == 201
    cat_id = cat_resp.get_json()["categoria"]["id"]

    # Cria produto
    prod_resp = client.post(
        "/api/produto/novo",
        json={
            "nome": "ProdutoVenda",
            "preco": 10.0,
            "quantidade_estoque": 100,
            "categoria_id": cat_id
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert prod_resp.status_code == 201
    prod_id = prod_resp.get_json()["produto"]["id"]

    # Cria cliente
    cli_resp = client.post(
        "/api/cliente/novo",
        json={"nome": "Cliente Venda", "email": "clientevenda@test.com"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert cli_resp.status_code == 201
    cli_data = cli_resp.get_json()
    client_id = cli_data["cliente"].get("id") if "cliente" in cli_data else None
    assert client_id is not None

    # Registra a venda
    venda_resp = client.post(
        "/api/venda/registrar",
        json={
            "cliente_id": client_id,
            "utilizador_id": user_id,
            "produto_id": prod_id,
            "quantidade": 2
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert venda_resp.status_code == 201
    data = venda_resp.get_json()
    assert "mensagem" in data
    assert data["mensagem"] == "Venda registrada com sucesso!"
    assert "venda" in data

def test_listar_vendas(client):
    # Faz login para obter um token válido
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # Mesmo que as rotas de vendas não requeiram token, incluímos o header para padronização
    resp = client.get(
        "/api/venda/lista",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "vendas" in data
    assert isinstance(data["vendas"], list)