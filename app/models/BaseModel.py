from sqlalchemy.inspection import inspect
from app.extensions import db
from app.utils.logger_util import get_logger

logger = get_logger(__name__)

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def to_dict(self, include_relationships: bool = True, backref: bool = False) -> dict:
        """
        Converte a instância do modelo em um dicionário, incluindo colunas e,
        opcionalmente, relacionamentos.

        :param include_relationships: se True, inclui objetos relacionados
        :param backref: usado internamente para evitar loops de relacionamento
        """
        try:
            mapper = inspect(self).mapper
            data = {}

            # colunas simples
            for column in mapper.column_attrs:
                data[column.key] = getattr(self, column.key)

            # se tiver relacionamento devolve o valor
            if include_relationships:
                for rel in mapper.relationships:
                    # evita loop de backref
                    if rel.back_populates and backref:
                        continue

                    value = getattr(self, rel.key)

                    # varios dict, lista de dicts
                    if isinstance(value, list):
                        data[rel.key] = [
                            item.to_dict(include_relationships=False, backref=True)
                            for item in value
                        ]

                    # so um dict
                    elif value is not None:
                        data[rel.key] = value.to_dict(include_relationships=False, backref=True)

                    #sem relacionamento
                    else:
                        data[rel.key] = None

            return data

        except Exception as e:
            logger.error(f"Erro ao converter objeto para dicionário: {e}", exc_info=True)
            return {"error": "Falha na conversão para JSON"}

    @classmethod
    def from_dict(cls, data):
        """Cria uma instância do modelo a partir de um dicionário"""
        try:
            return cls(**data)
        except Exception as e:
            logger.error(f"Erro ao criar instância via from_dict: {e}", exc_info=True)
            raise

    @staticmethod
    def create_tables():
        """Cria todas as tabelas no banco de dados (útil em testes)"""
        try:
            db.create_all()
            logger.info("Todas as tabelas foram criadas com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {e}", exc_info=True)
            raise
