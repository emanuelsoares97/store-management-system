from database import Base

class BaseModel(Base):
    __abstract__ = True  # ✅ Define que esta classe não vira tabela diretamente

    def to_dict(self):
        """Converte um objeto SQLAlchemy para dicionário JSON"""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    @classmethod
    def from_dict(cls, data):
        """Cria um objeto da classe a partir de um dicionário"""
        return cls(**data)
