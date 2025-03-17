from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from models.abstrata import BaseModel

class Venda(BaseModel.get_base()):  
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    utilizador_id = Column(Integer, ForeignKey("utilizadores.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    valor_total = Column(DECIMAL(10, 2), nullable=False)
    data_venda = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos 
    cliente = relationship("Cliente", backref="compras")
    utilizador = relationship("Utilizador", backref="vendas")
    produto = relationship("Produto", backref="vendas")
