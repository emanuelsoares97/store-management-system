from sqlalchemy import Column, Integer

class BaseModel:
    """Classe base abstrata para os modelos"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def get_base(cls):
        """Importa Database dentro do método para evitar import circular"""
        from database import Database
        return Database().Base


    def to_dict(self):
        """Converte um objeto SQLAlchemy para dicionário JSON"""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    @classmethod
    def from_dict(cls, data):
        """Cria um objeto da classe a partir de um dicionário"""
        return cls(**data)
