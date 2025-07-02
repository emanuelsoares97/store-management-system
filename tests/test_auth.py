import jwt
from datetime import datetime, timedelta, timezone
from config import Config


def test_login_admin(client):
    response = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.get_json()
    tokens = data["data"]

    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert "user" in tokens

    assert tokens["access_token"]
    assert tokens["refresh_token"]
    assert tokens["user"]["email"] == "admin@email.com"
    assert "id" in tokens["user"]
    assert "role" in tokens["user"]



def test_login_user(client):
    """Testa se o login de um utilizador comum funciona"""
    response = client.post("/api/auth/login", json={
        "email": "user@email.com",
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.get_json()
    tokens = data["data"]  # acessar a chave 'data'

    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert "user" in tokens
    assert tokens["access_token"]
    assert tokens["refresh_token"]
    assert tokens["user"]["email"] == "user@email.com"
    assert "id" in tokens["user"]
    assert "role" in tokens["user"]


def test_login_invalido(client):
    """Testa login com credenciais incorretas"""
    response = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "senhaerrada"
    })

    assert response.status_code == 403  # credenciais inválidas
    data = response.get_json()
    assert "message" in data


def test_logout_admin(client):
    # obtém token via login
    login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert login.status_code == 200
    token = login.get_json()["data"]["access_token"]  # corrigido para ['data']
    headers = {"Authorization": f"Bearer {token}"}

    # primeiro logout: deve retornar 200
    resp1 = client.post("/api/auth/logout", headers=headers)
    assert resp1.status_code == 200
    assert resp1.get_json()["message"] == "Logout bem-sucedido!"

    # segundo logout com mesmo token: deve retornar 401
    resp2 = client.post("/api/auth/logout", headers=headers)
    assert resp2.status_code == 401


def test_login_sem_email_ou_password(client):
    """Testa login sem email ou password"""
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data.get("message") == "Email e password são obrigatórios!"


def test_login_email_inexistente(client):
    """Testa login com email não cadastrado"""
    response = client.post("/api/auth/login", json={
        "email": "naoexiste@email.com",
        "password": "123456"
    })
    assert response.status_code == 403
    data = response.get_json()
    assert data.get("message") == "Credenciais inválidas"


def test_login_email_invalido(client):
    """Testa login com email em formato inválido"""
    response = client.post("/api/auth/login", json={
        "email": "email-invalido",
        "password": "123456"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data.get("message") == "Email inválido"


def test_login_metodo_http_errado(client):
    """Testa GET na rota de login"""
    response = client.get("/api/auth/login")
    assert response.status_code == 405  # método não permitido


def test_login_payload_invalido(client):
    """Testa envio de payload não-JSON"""
    response = client.post("/api/auth/login", data="texto sem JSON")
    assert response.status_code == 400
    data = response.get_json()
    assert data.get("message") == "Formato inválido, envie um JSON"


def test_login_token_expirado(client):
    """Testa rejeição de token expirado"""
    expired = datetime.now(timezone.utc) - timedelta(seconds=1)
    expired_token = jwt.encode({
        "id": 1,
        "email": "admin@email.com",
        "role": "admin",
        "exp": expired
    }, Config.SECRET_KEY, algorithm="HS256")

    response = client.get("/api/auth/auth", headers={
        "Authorization": f"Bearer {expired_token}"
    })
    assert response.status_code == 401


def test_login_token_invalido(client):
    """Testa rejeição de token inválido"""
    response = client.get("/api/auth/auth", headers={
        "Authorization": "Bearer token-falso"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data.get("message") == "Token inválido."


def test_logout_sem_token(client):
    """Testa logout sem token"""
    response = client.post("/api/auth/logout")
    assert response.status_code == 401
    data = response.get_json()

    assert data.get("message") == "Token em falta para logout"


def test_logout_com_token_revogado(client):
    """Testa logout com token já revogado"""
    login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    token = login.get_json()["data"]["access_token"]  # corrigido para ['data']
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/api/auth/logout", headers=headers)  # revoga token
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 401
    data = response.get_json()

    assert data.get("message") == "Token inválido. Faça login novamente."


def test_refresh_token_sucesso(client):
    """Testa renovação de access token"""
    login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    refresh_token = login.get_json()["data"]["refresh_token"]  # corrigido para ['data']

    response = client.post("/api/auth/refresh", headers={
        "Authorization": f"Bearer {refresh_token}"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data["data"]


def test_refresh_token_faltando(client):
    """Testa refresh sem token"""
    response = client.post("/api/auth/refresh")
    assert response.status_code == 401
    data = response.get_json()
    assert data.get("message") == "Refresh token é obrigatório!"


def test_refresh_token_expirado(client):
    """Testa rejeição de refresh token expirado"""
    expired = datetime.now(timezone.utc) - timedelta(seconds=1)
    expired_token = jwt.encode({"id": 1, "exp": expired}, Config.SECRET_KEY, algorithm="HS256")

    response = client.post("/api/auth/refresh", headers={
        "Authorization": f"Bearer {expired_token}"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data.get("message") == "Refresh token expirado. Faça login novamente!"


def test_refresh_token_invalido(client):
    """Testa rejeição de refresh token inválido"""
    response = client.post("/api/auth/refresh", headers={
        "Authorization": "Bearer token-falso"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data.get("message") == "Refresh token inválido!"
