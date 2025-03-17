
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.abstrata import BaseModel

class Categoria(BaseModel.get_base()):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False, unique=True)
    produtos = relationship("Produto", back_populates="categoria")
