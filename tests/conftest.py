import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from app import create_app
from config import TestConfig
from app.extensions import db
from app.models.User import User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="session")
def app():
    """
    Instância da aplicação para testes com banco em memória.
    Cria e destrói o esquema antes e depois da sessão de testes.
    """
    app = create_app(config_class=TestConfig)
    with app.app_context():
        # Cria todas as tabelas no banco de testes
        db.create_all()
        yield app
        # Limpa sessao e remove esquema após todos os testes
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    """
    Cliente HTTP para testar rotas Flask.
    """
    return app.test_client()

@pytest.fixture(scope="function", autouse=True)
def seed_users(app):
    """
    Semente de dados: cria Admin, Gerente e User antes de cada teste.
    """
    admin = User(
        name="Admin Teste",
        email="admin@email.com",
        password=generate_password_hash("123456"),
        role="admin"
    )
    gerente = User(
        name="Gerente Teste",
        email="gerente@email.com",
        password=generate_password_hash("123456"),
        role="gerente"
    )
    user = User(
        name="User Teste",
        email="user@email.com",
        password=generate_password_hash("123456"),
        role="user"
    )
    db.session.add_all([admin, gerente, user])
    db.session.commit()
    yield
    # Reverte alterações após cada teste
    db.session.rollback()
