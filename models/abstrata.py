from sqlalchemy import Column, Integer
from sqlalchemy.inspection import inspect
from util.logger_util import get_logger

logger = get_logger("BaseModel")

class BaseModel:
    """Classe base abstrata para os modelos"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    logger.info("Classe Abstrata iniciada")

    @classmethod
    def get_base(cls):
        """Importa Database dentro do método para evitar import circular"""
        try:
            from database import Database
            logger.debug("Database chamado.")
            return Database().Base
        except Exception as e:
            logger.error(f"Tentativa de importar Database, erro: {e}")
            raise ValueError(f"Tentativa de importar Database, erro: {str(e)}", exc_info=True)

    def to_dict(self):
        """Converte um objeto SQLAlchemy para dicionário JSON"""
        try:
            # Garante que a tabela foi inicializada corretamente
            if not hasattr(self, "__table__"):
                raise AttributeError("Modelo sem `__table__`, pode estar mal definido.")

            logger.info("Objeto convertido para JSON.")
            return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        except Exception as e:
            logger.error(f"Erro ao converter objeto para JSON: {str(e)}", exc_info=True)
            return {"erro": "Falha na conversão para JSON"}

    @classmethod
    def from_dict(cls, data):
        """Cria um objeto da classe a partir de um dicionário"""
        return cls(**data)
