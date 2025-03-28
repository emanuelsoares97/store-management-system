from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base 
import os
from app.util.logger_util import get_logger

logger = get_logger(__name__)

class Database:
    """Gerencia a conexão com o banco de dados."""
    _instance = None  

    def __new__(cls, db_url=None):
        """
        Cria uma nova instância da classe Database se ainda não existir
        ou se um db_url diferente for fornecido.

        Args:
            db_url (str, opcional): URL do banco de dados a ser utilizada.
                                    Se não fornecido, será utilizado o URL padrão.

        Returns:
            Database: Instância única da classe Database.
        """
        if cls._instance is None or (db_url and db_url != cls._instance.DB_URL):
            logger.info("Criando nova instância do Database.")
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.DB_URL = db_url if db_url else cls._get_default_db_url()
            logger.info(f"Usando o banco de dados: {cls._instance.DB_URL}")
            cls._instance.engine = create_engine(cls._instance.DB_URL, echo=False)
            cls._instance.SessionLocal = sessionmaker(bind=cls._instance.engine, autoflush=False, expire_on_commit=False)
            cls._instance.Base = Base
        else:
            logger.debug("Utilizando instância existente do Database.")
        return cls._instance

    @staticmethod
    def _get_default_db_url():
        """
        Gera e retorna o URL padrão para o banco de dados SQLite.

        Returns:
            str: URL do banco de dados SQLite.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(base_dir, "db")
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "database.db")
        default_url = f"sqlite:///{db_path}"
        logger.info(f"URL padrão do banco de dados gerada: {default_url}")
        return default_url

    @classmethod
    def get_session(cls):
        """
        Retorna uma sessão do banco de dados para executar operações.

        Returns:
            Session: Objeto de sessão para interagir com o banco de dados.
        """
        logger.debug("Obtendo uma nova sessão do banco de dados.")
        return cls().SessionLocal()

    @classmethod
    def registrar_modelos(cls):
        """
        Cria as tabelas no banco de dados com base nos modelos registrados (Base).
        Se a instância do Database não existir, ela será criada.
        """
        if cls._instance is None:
            logger.debug("Instância do Database não encontrada. Criando nova instância para registrar modelos.")
            cls()
        logger.info("Registrando modelos e criando tabelas, se necessário.")
        cls._instance.Base.metadata.create_all(cls._instance.engine)
    
    @classmethod
    def reset_instance(cls):
        """
        Reseta a instância do Database (útil para testes).

        Após chamar este método, uma nova instância será criada na próxima vez que Database() for invocado.
        """
        logger.info("Resetando a instância do Database.")
        cls._instance = None
