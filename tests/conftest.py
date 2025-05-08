import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
from app.database import Database
from app.models.basemodel import BaseModel
from config import TestConfig
from app.models.user import Utilizador
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="session")
def app():
    # Reseta a instância do Database para garantir que usamos o TestConfig
    Database.reset_instance()
    
    app = create_app(config_class=TestConfig)
    with app.app_context():
        BaseModel.criar_tabelas()  # Cria as tabelas usando a instância atual
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope="function", autouse=True)
def criar_utilizador_admin_gerente_user():
    """Cria utilizadores de teste"""
    session = Database.get_session()

    admin = Utilizador(
        nome="Admin Teste",
        email="admin@email.com",
        password=generate_password_hash("123456"),
        role="admin"
    )

    gerente = Utilizador(
        nome="Gerente Teste",
        email="gerente@email.com",
        password=generate_password_hash("123456"),
        role="gerente"
    )

    user = Utilizador(
        nome="User Teste",
        email="user@email.com",
        password=generate_password_hash("123456"),
        role="user"
    )

    session.add_all([admin, gerente, user])
    session.commit()

    yield  # Permite que os testes usem os usuários criados

    session.rollback()
    session.close()
