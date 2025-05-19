from app.models.Sale import Sale
from app.models.Product import Product
from app.extensions import db
from app.util.logger_util import get_logger

logger = get_logger(__name__)

class SaleService:
    """Gerencia as vendas no sistema"""

    @classmethod
    def list_sales(cls) -> list:
        """Lista todas as vendas"""
        sales = Sale.query.all()
        logger.info(f"Lista de vendas carregadas, com {len(sales)} vendas.")
        return {"sales": [sale.to_dict() for sale in sales]}, 200

    @classmethod
    def register_sale(cls, customer_id, user_id, product_id, quantity):
        """Registra uma nova venda"""
        product = Product.query.get(product_id)
        if not product:
            logger.warning(f"Produto com ID {product_id} não encontrado.")
            return {"erro": "Produto não encontrado!"}, 404

        if quantity <= 0:
            logger.warning("A quantidade deve ser maior que zero!")
            return {"erro": "A quantidade deve ser maior que zero!"}, 400

        if product.stock_quantity < quantity:
            logger.warning("Estoque insuficiente para essa venda!")
            return {"erro": "Estoque insuficiente para essa venda!"}, 400

        try:
            total_value = product.price * quantity
            new_sale = Sale(
                customer_id=customer_id,
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                total_value=total_value
            )
            db.session.add(new_sale)
            product.stock_quantity -= quantity
            db.session.commit()
            db.session.refresh(new_sale)

            logger.info(
                f"Venda registrada: Cliente {customer_id}, Produto {product_id}, Quantidade {quantity}"
            )
            return new_sale.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao registrar venda: {e}")
            return {"erro": "Erro ao registrar venda"}, 500
