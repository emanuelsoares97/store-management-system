from app.models.sale import Venda
from app.models.product import Produto
from app.database import Database
from app.util.logger_util import get_logger

class VendaService:
    """Gerencia as vendas no sistema"""
    
    logger = get_logger(__name__)

    @classmethod
    def list_vendas(cls):
        """Lista todas as vendas"""
        session = Database.get_session()
        try:
            vendas = session.query(Venda).all()
            cls.logger.info(f"Lista de vendas carregadas, com {len(vendas)} vendas.")
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
                cls.logger.info(f"Tentativa de procurar produto não registado, {produto_id}.")
                raise ValueError("Produto não encontrado!")

            if quantidade <= 0:
                cls.logger.warning("A quantidade deve ser maior que zero!")
                raise ValueError("A quantidade deve ser maior que zero!")

            if produto.quantidade_estoque < quantidade:
                cls.logger.warning("Estoque insuficiente para essa venda!")
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
