from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.abstrata import BaseModel
from app.util.logger_util import get_logger

logger=get_logger(__name__)

class Categoria(BaseModel):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False, unique=True)
    produtos = relationship("Produto", back_populates="categoria")