import requests

def test_login(client):
    """Testa se o login retorna um access token e um refresh token válidos"""
    response = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })

    assert response.status_code == 200  # Verifica se o status HTTP está correto

    json_data = response.json  # Captura o JSON da resposta

    assert "access_token" in json_data  # Verifica se há um access token
    assert "refresh_token" in json_data  # Verifica se há um refresh token
    assert "utilizador" in json_data  # Verifica se há os dados do utilizador

    assert json_data["access_token"]  # Garante que o access token não está vazio
    assert json_data["refresh_token"]  # Garante que o refresh token não está vazio

    # Valida se os dados do utilizador foram retornados corretamente
    assert json_data["utilizador"]["email"] == "admin@email.com"
    assert "id" in json_data["utilizador"]
    assert "role" in json_data["utilizador"]

def test_login_invalido(client):
    """Testa login com credenciais erradas"""
    response = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "senhaErrada"
    })

    assert response.status_code == 403  # esperar um erro de login invalido
    assert "erro" in response.json


def test_rota_protegida(client):
    """Testa se uma rota protegida retorna 200 com token válido"""

    # 1️⃣ Primeiro, faz login e pega o token
    response_login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert response_login.status_code == 200
    access_token = response_login.json["access_token"]

    # 2️⃣ Agora, faz um GET numa rota protegida usando o token
    response = client.get("/api/produto/ativos", headers={"Authorization": f"Bearer {access_token}"})

    # 3️⃣ Valida se a resposta foi bem-sucedida
    assert response.status_code == 200
    assert "produtos" in response.json  # ✅ Garante que a chave 'produtos' existe na resposta.
    assert isinstance(response.json["produtos"], list)  # ✅ Agora verificamos corretamente a lista.

