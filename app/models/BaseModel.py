from sqlalchemy import Column, Integer
from sqlalchemy.inspection import inspect
from app.util.logger_util import get_logger
from base import Base  # Base declarativa definida externamente

logger = get_logger(__name__)

class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    logger.debug("Classe BaseModel carregada.")

    def to_dict(self):
        """Converte a instância do modelo em um dicionário"""
        try:
            if not hasattr(self, "__table__"):
                raise AttributeError("Modelo sem `__table__`, pode estar mal definido.")
            
            return {
                c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs
            }

        except Exception as e:
            logger.error(f"Erro ao converter objeto para dicionário: {e}", exc_info=True)
            return {"erro": "Falha na conversão para JSON"}

    @classmethod
    def from_dict(cls, data):
        """Cria uma instância do modelo a partir de um dicionário"""
        try:
            return cls(**data)
        except Exception as e:
            logger.error(f"Erro ao criar instância via from_dict: {e}", exc_info=True)
            raise

    @classmethod
    def get_base(cls):
        """Retorna o declarative base utilizado"""
        return Base

    @classmethod
    def create_table(cls):
        """Cria a tabela do modelo no banco de dados (útil em testes)"""
        try:
            from app.database import Database
            engine = Database.get_session().get_bind()
            cls.get_base().metadata.create_all(engine)
            logger.info(f"Tabela criada para {cls.__name__}.")
        except Exception as e:
            logger.error(f"Erro ao criar tabela para {cls.__name__}: {e}", exc_info=True)
            raise
