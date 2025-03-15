from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from models.abstrata import BaseModel

class Venda(BaseModel):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("utilizadores.id"), nullable=False)  # Cliente que comprou
    utilizador_id = Column(Integer, ForeignKey("utilizadores.id"), nullable=False)  # Vendedor
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)  # Produto vendido
    quantidade = Column(Integer, nullable=False)
    valor_total = Column(Float, nullable=False)
    data_venda = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    cliente = relationship("Utilizador", foreign_keys=[cliente_id])
    utilizador = relationship("Utilizador", foreign_keys=[utilizador_id])
    produto = relationship("Produto")

