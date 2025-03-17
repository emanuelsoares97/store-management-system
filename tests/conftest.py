import pytest
from app import create_app
from models.abstrata import BaseModel
from models.utilizador import Utilizador
from database import Database
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    """Cria e configura uma instância do Flask para testes"""
    app = create_app()
    with app.app_context():
        BaseModel.criar_tabelas()  # ✅ Cria tabelas para os testes
        criar_utilizador_admin()  # ✅ Garante que o admin existe nos testes
        yield app
        Database.get_session().rollback()  # ✅ Evita que dados fiquem salvos entre testes

def criar_utilizador_admin():
    """Cria um utilizador admin para os testes"""
    session = Database.get_session()
    if not session.query(Utilizador).filter_by(email="admin@email.com").first():
        admin = Utilizador(
            nome="Admin Teste",
            email="admin@email.com",
            password=generate_password_hash("123456"),  # ✅ Senha para testes
            role="admin"
        )
        session.add(admin)
        session.commit()

@pytest.fixture
def client(app):
    """Retorna um cliente de teste do Flask"""
    return app.test_client()
