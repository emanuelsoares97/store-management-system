from app.models.Sale import Sale
from app.models.Product import Product
from app.database import Database
from app.util.logger_util import get_logger

class SaleService:
    """Gerencia as vendas no sistema"""

    logger = get_logger(__name__)

    @classmethod
    def list_sales(cls):
        """Lista todas as vendas"""
        session = Database.get_session()
        try:
            sales = session.query(Sale).all()
            cls.logger.info(f"Lista de vendas carregadas, com {len(sales)} vendas.")
            return {"sales": [sale.to_dict() for sale in sales]}, 200
        finally:
            session.close()

    @classmethod
    def register_sale(cls, customer_id, user_id, product_id, quantity):
        """Registra uma nova venda"""
        session = Database.get_session()
        try:
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                cls.logger.warning(f"Produto com ID {product_id} não encontrado.")
                return {"erro": "Produto não encontrado!"}, 404

            if quantity <= 0:
                cls.logger.warning("A quantidade deve ser maior que zero!")
                return {"erro": "A quantidade deve ser maior que zero!"}, 400

            if product.stock_quantity < quantity:
                cls.logger.warning("Estoque insuficiente para essa venda!")
                return {"erro": "Estoque insuficiente para essa venda!"}, 400

            total_value = product.price * quantity

            new_sale = Sale(
                customer_id=customer_id,
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                total_value=total_value
            )
            session.add(new_sale)
            product.stock_quantity -= quantity
            session.commit()
            session.refresh(new_sale)

            cls.logger.info(f"Venda registrada: Cliente {customer_id}, Produto {product_id}, Quantidade {quantity}")
            return new_sale.to_dict(), 201

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao registrar venda: {e}")
            return {"erro": "Erro ao registrar venda"}, 500
        finally:
            session.close()
