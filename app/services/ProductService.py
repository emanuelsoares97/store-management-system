from app.models.Product import Product
from app.extensions import db
from app.utils.logger_util import get_logger
from app.utils.responses import success_response, error_response

logger = get_logger(__name__)

class ProductService:
    @classmethod
    def list_products(cls, only_actives=True):
        query = Product.query
        if only_actives:
            query = query.filter_by(active=True)
        products = query.all()
        return success_response({"products": [p.to_dict() for p in products]})

    @classmethod
    def create_product(cls, name, price, stock_quantity, category_id):

        if not name or price is None or stock_quantity is None or not category_id:
            return error_response("Nome, preço, estoque e categoria são obrigatórios!", 400)
        
        if price < 0 or stock_quantity < 0:
            return error_response("Preço e estoque devem ser valores positivos!", 400)
        
        if Product.query.filter_by(name=name).first():
            return error_response("Já existe um produto com esse nome!", 409)
        try:
            new_product = Product(
                name=name,
                price=price,
                stock_quantity=stock_quantity,
                category_id=category_id,
                active=True
            )
            db.session.add(new_product)
            db.session.commit()
            db.session.refresh(new_product)
            return success_response({"product": new_product.to_dict()}, "Produto criado com sucesso!", 201)
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar produto: {e}")
            return error_response("Erro ao criar produto", 500)

    @classmethod
    def update_product(cls, product_id, name=None, price=None, stock_quantity=None, active=None, category_id=None):
        product = Product.query.get(product_id)
        if not product:
            return error_response("Produto não encontrado!", 404)
        if name:
            product.name = name
        if price is not None:
            if price < 0:
                return error_response("O preço não pode ser negativo!", 400)
            product.price = price
        if stock_quantity is not None:
            if stock_quantity < 0:
                return error_response("O estoque não pode ser negativo!", 400)
            product.stock_quantity = stock_quantity
        if active is not None:
            product.active = active
        if category_id:
            product.category_id = category_id
        try:
            db.session.commit()
            return success_response({"product": product.to_dict()}, "Produto editado com sucesso!", 201)
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar produto: {e}")
            return error_response("Erro ao atualizar produto", 500)

    @classmethod
    def desactivate_product(cls, product_id):
        product = Product.query.get(product_id)
        if not product:
            return error_response("Produto não encontrado!", 404)
        if not product.active:
            return error_response("O produto já está desativado!", 400)
        product.active = False
        db.session.commit()
        return success_response(message=f"Produto '{product.name}' foi desativado com sucesso.")

    @classmethod
    def reactivate_product(cls, product_id):
        product = Product.query.get(product_id)
        if not product:
            return error_response("Produto não encontrado!", 404)
        if product.active:
            return error_response("O produto já está ativo!", 400)
        product.active = True
        db.session.commit()
        return success_response(message=f"Produto '{product.name}' foi reativado com sucesso.")
