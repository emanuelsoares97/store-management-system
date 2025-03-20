import jwt
from datetime import datetime, timedelta
from config import Config


def test_login_admin(client):
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

def test_login_user(client):
    """Testa se o login retorna um access token e um refresh token válidos"""
    response = client.post("/api/auth/login", json={
        "email": "user@email.com",
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
    assert json_data["utilizador"]["email"] == "user@email.com"
    assert "id" in json_data["utilizador"]
    assert "role" in json_data["utilizador"]

def test_login_invalido(client):
    """Testa login com credenciais erradas"""
    response = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "teste errado"
    })

    assert response.status_code == 403  # esperar um erro de login invalido
    assert "erro" in response.json

def test_logout_admin(client):
    """Testa se o logout revoga o token corretamente"""

    # 1️⃣ Login para obter um token válido
    login_response = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })

    assert login_response.status_code == 200  # Verifica se o login foi bem-sucedido

    json_data = login_response.get_json()  # Obtém o JSON corretamente

    assert "access_token" in json_data  # Verifica se há um access token
    assert json_data["access_token"]  # Garante que o access token não está vazio

    access_token = json_data["access_token"]  # Guarda o token para reutilizar

    # 2️⃣ Logout usando o token
    logout_response = client.post("/api/auth/logout", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert logout_response.status_code == 200  # Verifica se o logout foi bem-sucedido
    assert logout_response.get_json()["mensagem"] == "Logout bem-sucedido!"

def test_login_sem_email_ou_senha(client):
    """Testa login sem enviar email ou senha"""
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 400
    assert "erro" in response.get_json()
    assert response.get_json()["erro"] == "Email e senha são obrigatórios!"

def test_login_email_inexistente(client):
    """Testa login com um email que não existe"""
    response = client.post("/api/auth/login", json={
        "email": "naoexiste@email.com",
        "password": "123456"
    })
    assert response.status_code == 403
    assert "erro" in response.get_json()
    assert response.get_json()["erro"] == "Credenciais inválidas"

def test_login_senha_incorreta(client):
    """Testa login com senha errada"""
    response = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "senhaerrada"
    })
    assert response.status_code == 403
    assert "erro" in response.get_json()
    assert response.get_json()["erro"] == "Credenciais inválidas"

def test_login_email_invalido(client):
    """Testa login com email em formato inválido"""
    response = client.post("/api/auth/login", json={
        "email": "email-invalido",
        "password": "123456"
    })
    assert response.status_code == 400
    assert "erro" in response.get_json()
    assert response.get_json()["erro"] == "Email inválido"

def test_login_metodo_http_errado(client):
    """Testa se o login retorna erro ao usar GET em vez de POST"""
    response = client.get("/api/auth/login")
    assert response.status_code == 405  # Method Not Allowed

def test_login_payload_invalido(client):
    """Testa login sem enviar um JSON válido"""
    response = client.post("/api/auth/login", data="texto sem JSON")
    assert response.status_code == 400
    assert "erro" in response.get_json()
    assert response.get_json()["erro"] == "Formato inválido, envie um JSON"

def test_login_token_expirado(client):
    """Testa se um token expirado não é aceito"""
    expired_token = jwt.encode({
        "id": 1,
        "email": "admin@email.com",
        "role": "admin",
        "exp": datetime.now() - timedelta(seconds=1)  # Já expirado!
    }, Config.SECRET_KEY, algorithm="HS256")

    response = client.get("/api/auth/auth", headers={
        "Authorization": f"Bearer {expired_token}"
    })
    assert response.status_code == 401  # Token deve ser recusado
    assert "Alerta" in response.get_json()
    assert response.get_json()["Alerta"] == "Token expirado. Faça login novamente."

def test_login_token_invalido(client):
    """Testa se um token inválido é rejeitado"""
    response = client.get("/api/auth/auth", headers={
        "Authorization": "Bearer token-falso-aleatorio"
    })
    assert response.status_code == 401  # Deve ser recusado
    assert "Alerta" in response.get_json()
    assert response.get_json()["Alerta"] == "Token inválido."

def test_logout_sem_token(client):
    """Testa se o logout retorna erro quando nenhum token é enviado"""
    response = client.post("/api/auth/logout")  # Sem token
    assert response.status_code == 401  # Deve falhar
    assert "Alerta" in response.get_json()
    assert response.get_json()["Alerta"] == "Token em falta"

def test_logout_com_token_revogado(client):
    """Testa se um token já revogado não pode ser reutilizado"""
    
    # 1️⃣ Login para obter um token válido
    login_response = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert login_response.status_code == 200
    access_token = login_response.get_json()["access_token"]

    # 2️⃣ Logout usando o token
    logout_response = client.post("/api/auth/logout", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert logout_response.status_code == 200

    # 3️⃣ Tenta deslogar de novo com o mesmo token (deve falhar)
    response_reuso = client.post("/api/auth/logout", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response_reuso.status_code == 401  # Não pode reutilizar token revogado
    assert "Alerta" in response_reuso.get_json()
    assert response_reuso.get_json()["Alerta"] == "Token inválido. Faça login novamente."

def test_refresh_token_sucesso(client):
    """Testa se o refresh token gera um novo access token"""
    
    # 1️⃣ Login para obter um refresh token válido
    login_response = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert login_response.status_code == 200  # Login deve ser bem-sucedido
    json_data = login_response.get_json()

    refresh_token = json_data["refresh_token"]  # Obtém o refresh token

    # 2️⃣ Solicita a renovação do access token
    response = client.post("/api/auth/refresh", headers={
        "Authorization": f"Bearer {refresh_token}"
    })
    assert response.status_code == 200  # Deve renovar o token com sucesso
    json_data = response.get_json()
    
    assert "access_token" in json_data  # Deve retornar um novo access token
    assert json_data["access_token"]  # O token não deve estar vazio

def test_refresh_token_faltando(client):
    """Testa se a API retorna erro quando o refresh token não é enviado"""
    
    response = client.post("/api/auth/refresh")  # Sem token no header
    assert response.status_code == 401  # Deve falhar
    assert "erro" in response.get_json()
    assert response.get_json()["erro"] == "Refresh token é obrigatório!"

def test_refresh_token_expirado(client):
    """Testa se um refresh token expirado é rejeitado"""
    
    # 1️⃣ Gera um refresh token que já expirou
    expired_token = jwt.encode({
        "id": 1,
        "exp": datetime.now() - timedelta(seconds=1)  # Token já expirado!
    }, Config.SECRET_KEY, algorithm="HS256")

    # 2️⃣ Tenta renovar o access token com um refresh token expirado
    response = client.post("/api/auth/refresh", headers={
        "Authorization": f"Bearer {expired_token}"
    })
    
    assert response.status_code == 401  # Deve falhar
    assert "erro" in response.get_json()
    assert response.get_json()["erro"] == "Refresh token expirado. Faça login novamente!"

def test_refresh_token_invalido(client):
    """Testa se um refresh token inválido é rejeitado"""
    
    response = client.post("/api/auth/refresh", headers={
        "Authorization": "Bearer token-falso-aleatorio"
    })
    
    assert response.status_code == 401  # Deve falhar
    assert "erro" in response.get_json()
    assert response.get_json()["erro"] == "Refresh token inválido!"

