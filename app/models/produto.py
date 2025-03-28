from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.abstrata import BaseModel

class Produto(BaseModel):  
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True, index=True)  # Nome deve ser único para evitar duplicações
    descricao = Column(Text, nullable=True)  # Descrição detalhada do produto
    preco = Column(Float, nullable=False)
    quantidade_estoque = Column(Integer, nullable=False)  # Controle de estoque
    ativo = Column(Boolean, default=True)  # Indica se o produto está ativo ou inativo
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)  # Relacionamento com Categoria
    categoria = relationship("Categoria", back_populates="produtos")  # Relacionamento ORM
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Data de criação
    atualizado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))  # Data de atualização

