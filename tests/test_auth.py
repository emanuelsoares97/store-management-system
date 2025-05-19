import jwt
from datetime import datetime, timedelta, timezone
from config import Config


def test_login_admin(client):
    """Testa se o login retorna access e refresh tokens, além dos dados do utilizador"""
    response = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })

    assert response.status_code == 200  # verifica status HTTP correto
    data = response.get_json()

    assert "access_token" in data  # verifica access token
    assert "refresh_token" in data  # verifica refresh token
    assert "user" in data  # verifica dados do utilizador

    assert data["access_token"]  # garante token não vazio
    assert data["refresh_token"]

    assert data["user"]["email"] == "admin@email.com"  # confere email
    assert "id" in data["user"]
    assert "role" in data["user"]


def test_login_user(client):
    """Testa se o login de um utilizador comum funciona"""
    response = client.post("/api/auth/login", json={
        "email": "user@email.com",
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.get_json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert "user" in data
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["user"]["email"] == "user@email.com"
    assert "id" in data["user"]
    assert "role" in data["user"]


def test_login_invalido(client):
    """Testa login com credenciais incorretas"""
    response = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "senhaerrada"
    })

    assert response.status_code == 403  # credenciais inválidas
    data = response.get_json()
    assert "erro" in data


def test_logout_admin(client):
    # obtém token via login
    login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    assert login.status_code == 200
    token = login.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # primeiro logout: deve retornar 200
    resp1 = client.post("/api/auth/logout", headers=headers)
    assert resp1.status_code == 200
    assert resp1.get_json()["message"] == "Logout bem-sucedido!"

    # segundo logout com mesmo token: deve retornar 401
    resp2 = client.post("/api/auth/logout", headers=headers)
    assert resp2.status_code == 401


def test_login_sem_email_ou_senha(client):
    """Testa login sem email ou senha"""
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data.get("erro") == "Email e senha são obrigatórios!"


def test_login_email_inexistente(client):
    """Testa login com email não cadastrado"""
    response = client.post("/api/auth/login", json={
        "email": "naoexiste@email.com",
        "password": "123456"
    })
    assert response.status_code == 403
    data = response.get_json()
    assert data.get("erro") == "Credenciais inválidas"


def test_login_email_invalido(client):
    """Testa login com email em formato inválido"""
    response = client.post("/api/auth/login", json={
        "email": "email-invalido",
        "password": "123456"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data.get("erro") == "Email inválido"


def test_login_metodo_http_errado(client):
    """Testa GET na rota de login"""
    response = client.get("/api/auth/login")
    assert response.status_code == 405  # método não permitido


def test_login_payload_invalido(client):
    """Testa envio de payload não-JSON"""
    response = client.post("/api/auth/login", data="texto sem JSON")
    assert response.status_code == 400
    data = response.get_json()
    assert data.get("erro") == "Formato inválido, envie um JSON"


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
    assert data.get("Alerta") == "Token inválido."


def test_logout_sem_token(client):
    """Testa logout sem token"""
    response = client.post("/api/auth/logout")
    assert response.status_code == 401
    data = response.get_json()
    assert data.get("Alerta") == "Token em falta"


def test_logout_com_token_revogado(client):
    """Testa logout com token já revogado"""
    login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    token = login.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/api/auth/logout", headers=headers)  # revoga token
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 401
    data = response.get_json()
    assert data.get("Alerta") == "Token inválido. Faça login novamente."


def test_refresh_token_sucesso(client):
    """Testa renovação de access token"""
    login = client.post("/api/auth/login", json={
        "email": "admin@email.com",
        "password": "123456"
    })
    refresh_token = login.get_json()["refresh_token"]

    response = client.post("/api/auth/refresh", headers={
        "Authorization": f"Bearer {refresh_token}"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data


def test_refresh_token_faltando(client):
    """Testa refresh sem token"""
    response = client.post("/api/auth/refresh")
    assert response.status_code == 401
    data = response.get_json()
    assert data.get("erro") == "Refresh token é obrigatório!"


def test_refresh_token_expirado(client):
    """Testa rejeição de refresh token expirado"""
    expired = datetime.now(timezone.utc) - timedelta(seconds=1)
    expired_token = jwt.encode({"id": 1, "exp": expired}, Config.SECRET_KEY, algorithm="HS256")

    response = client.post("/api/auth/refresh", headers={
        "Authorization": f"Bearer {expired_token}"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data.get("erro") == "Refresh token expirado. Faça login novamente!"


def test_refresh_token_invalido(client):
    """Testa rejeição de refresh token inválido"""
    response = client.post("/api/auth/refresh", headers={
        "Authorization": "Bearer token-falso"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data.get("erro") == "Refresh token inválido!"
