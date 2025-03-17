from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from werkzeug.security import generate_password_hash

class Database:
    """Classe Singleton para gerenciar a conexão com o banco de dados"""
    _instance = None  

    # Caminho seguro para o banco de dados
    pasta_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db")
    os.makedirs(pasta_db, exist_ok=True)

    DB_URL = f"sqlite:///{pasta_db}/database.db"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.engine = create_engine(cls.DB_URL, echo=False)  # 🔹 echo=False para produção
            cls._instance.SessionLocal = sessionmaker(bind=cls._instance.engine, autoflush=False, expire_on_commit=False)
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

        from models.utilizador import Utilizador  # Importação atrasada para evitar erro de dependência

        session = cls.get_session()
        try:
            # Criar admin apenas se a tabela estiver vazia
            if session.query(Utilizador).count() == 0:
                admin = Utilizador(
                    nome="admin",
                    email="admin@email.com",
                    password=generate_password_hash("123456"),
                    role="admin"
                )
                session.add(admin)
                session.commit()
                print("Administrador padrão criado.")

        except Exception as e:
            print(f"Erro ao registrar admin: {e}")
            session.rollback()
        finally:
            session.close()

# Criar instância da base para ser usada nos modelos
Base = Database().Base

