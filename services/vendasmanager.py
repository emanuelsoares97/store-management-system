from models.vendas import Venda
from models.produto import Produto
from database import Database
import logging

class VendaService:
    """Gerencia as vendas no sistema"""
    
    logger = logging.getLogger("VendaService")

    @classmethod
    def listar_vendas(cls):
        """Lista todas as vendas"""
        session = Database.get_session()
        try:
            vendas = session.query(Venda).all()
            return [venda.to_dict() for venda in vendas]
        finally:
            session.close()

    @classmethod
    def registrar_venda(cls, cliente_id, utilizador_id, produto_id, quantidade):
        """Registra uma nova venda"""
        session = Database.get_session()
        try:
            produto = session.query(Produto).filter_by(id=produto_id).first()
            if not produto:
                raise ValueError("Produto não encontrado!")

            if quantidade <= 0:
                raise ValueError("A quantidade deve ser maior que zero!")

            if produto.quantidade_estoque < quantidade:
                raise ValueError("Estoque insuficiente para essa venda!")

            valor_total = produto.preco * quantidade

            nova_venda = Venda(
                cliente_id=cliente_id,
                utilizador_id=utilizador_id,
                produto_id=produto_id,
                quantidade=quantidade,
                valor_total=valor_total
            )
            session.add(nova_venda)
            produto.quantidade_estoque -= quantidade  # Atualiza o estoque do produto
            session.commit()
            session.refresh(nova_venda)

            cls.logger.info(f"Venda registrada: Cliente {cliente_id}, Produto {produto_id}, Quantidade {quantidade}")
            return nova_venda.to_dict()

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao registrar venda: {e}")
            raise Exception("Erro ao registrar venda")
        finally:
            session.close()
