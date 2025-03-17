from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.abstrata import BaseModel

class Produto(BaseModel.get_base()):  
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True, index=True)  # Nome deve ser único para evitar duplicações
    descricao = Column(Text, nullable=True)  # Descrição detalhada do produto
    preco = Column(Float, nullable=False)
    quantidade_estoque = Column(Integer, nullable=False, default=0)  # Controle de estoque
    ativo = Column(Boolean, default=True)  # Indica se o produto está ativo ou inativo
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)  # Relacionamento com Categoria
    categoria = relationship("Categoria", back_populates="produtos")  # Relacionamento ORM
    criado_em = Column(DateTime, default=datetime.utcnow)  # Data de criação
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de atualização

