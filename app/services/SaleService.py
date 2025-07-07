from app.models.Sale import Sale
from app.models.Product import Product
from app.extensions import db
from app.utils.logger_util import get_logger
from app.utils.responses import success_response, error_response
from app.services.CustomerService import CustomerService

logger = get_logger(__name__)

class SaleService:
    @classmethod
    def list_sales(cls):
        sales = Sale.query.all()
        logger.info(f"Lista de vendas carregadas: {len(sales)} registros.")
        return success_response({"sales": [s.to_dict() for s in sales]})

    @classmethod
    def register_sale(cls, customer_data, user_id, product_id, quantity):
        try:
            # Converte os dados recebidos do frontend para os tipos corretos
            product_id = int(product_id)
            quantity = int(quantity)
        except (TypeError, ValueError):
            logger.warning("product_id ou quantity inválidos.")
            return error_response("Dados inválidos: product_id e quantity devem ser numéricos.", 400)

        # obtém ou cria cliente (pode ser Guest)
        customer = CustomerService.find_or_create(
            name=customer_data.get("name"),
            email=customer_data.get("email"),
            phone=customer_data.get("phone")
        )
        if not customer:
            return error_response("Erro ao obter/criar cliente.", 500)

        # valida produto
        product = db.session.get(Product, product_id)
        if not product:
            logger.warning(f"Produto ID {product_id} não encontrado.")
            return error_response("Produto não encontrado!", 404)
        if quantity <= 0:
            logger.warning("Quantidade deve ser maior que zero.")
            return error_response("Quantidade inválida!", 400)
        if product.stock_quantity < quantity:
            logger.warning("Estoque insuficiente.")
            return error_response("Estoque insuficiente!", 400)

        try:
            total_value = product.price * quantity
            new_sale = Sale(
                customer_id=customer.id,
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                total_value=total_value
            )
            db.session.add(new_sale)
            product.stock_quantity -= quantity
            db.session.commit()
            db.session.refresh(new_sale)

            logger.info(f"Venda registrada: Cliente {customer.name}, Produto {product.name}, Quantidade {quantity}")
            return success_response({"sale": new_sale.to_dict()}, "Venda registrada com sucesso!", 201)
        except Exception as e:
            db.session.rollback()
            import traceback
            print("ERRO AO EDITAR PRODUTO:")
            traceback.print_exc()  # Mostra o erro completo no terminal
            logger.error(f"Erro ao registrar venda: {e}", exc_info=True)
            return error_response("Erro ao registrar venda", 500)
