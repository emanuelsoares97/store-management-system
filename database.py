from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

class Database:
    """Classe Singleton para gerenciar a conexão com o banco de dados"""
    _instance = None  

    pasta_db = os.path.join(os.getcwd(), "db")
    os.makedirs(pasta_db, exist_ok=True)

    DB_URL = f"sqlite:///{pasta_db}/database.db"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.engine = create_engine(cls.DB_URL, echo=True)
            cls._instance.SessionLocal = sessionmaker(bind=cls._instance.engine)
            cls._instance.Base = declarative_base()
        return cls._instance

    @classmethod
    def get_session(cls):
        """Retorna uma nova sessão do banco de dados"""
        return cls().SessionLocal()

    @classmethod
    def registrar_modelos(cls):
        """Cria as tabelas e garante que um admin existe"""
        instancia = cls()  
        instancia.Base.metadata.create_all(bind=instancia.engine)

        # Evita importar antes do SQLAlchemy estar pronto
        from models.utilizador import Utilizador
        from werkzeug.security import generate_password_hash

        session = cls.get_session()

        # Verifica se já existe um admin
        if not session.query(Utilizador).filter_by(nome="admin").first():
            admin = Utilizador(
                nome="admin",
                email="admin@email.com",
                password=generate_password_hash("123456"),
                role="admin"
            )
            session.add(admin)
            session.commit()
            print("Administrador padrão criado.")

# Criar instância da base para ser usada nos modelos
Base = Database().Base

