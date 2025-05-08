from app.models.Product import Product
from app.database import Database
from app.util.logger_util import get_logger

class ProductService:
    """Classe responsável pelo gerenciamento de produtos no banco de dados"""

    logger = get_logger(__name__)

    @classmethod
    def list_products(cls, only_actives=True):
        """Retorna a lista de produtos (ativos por padrão)"""
        session = Database.get_session()
        try:
            query = session.query(Product)
            if only_actives:
                query = query.filter_by(active=True)
            products = query.all()
            return {"produtos": [product.to_dict() for product in products]}, 200
        finally:
            session.close()

    @classmethod
    def create_product(cls, name, price, stock_quantity, category_id):
        """Cria e adiciona um novo produto no banco de dados"""
        session = Database.get_session()
        try:
            if not name or price is None or stock_quantity is None or not category_id:
                return {"erro": "Nome, preço, estoque e categoria são obrigatórios!"}, 400

            if price < 0 or stock_quantity < 0:
                return {"erro": "Preço e estoque devem ser valores positivos!"}, 400

            existing_product = session.query(Product).filter_by(name=name).first()
            if existing_product:
                return {"erro": "Já existe um produto com esse nome!"}, 409

            new_product = Product(
                name=name,
                price=price,
                stock_quantity=stock_quantity,
                category_id=category_id,
                active=True
            )
            session.add(new_product)
            session.commit()
            session.refresh(new_product)

            return new_product.to_dict(), 201

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao criar produto: {e}")
            return {"erro": "Erro ao criar produto"}, 500
        finally:
            session.close()

    @classmethod
    def update_product(cls, product_id, name=None, price=None, stock_quantity=None, active=None, category_id=None):
        """Atualiza um produto pelo ID"""
        session = Database.get_session()
        try:
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                return {"erro": "Produto não encontrado!"}, 404

            if name:
                product.name = name
            if price is not None:
                if price < 0:
                    return {"erro": "O preço não pode ser negativo!"}, 400
                product.price = price
            if stock_quantity is not None:
                if stock_quantity < 0:
                    return {"erro": "O estoque não pode ser negativo!"}, 400
                product.stock_quantity = stock_quantity
            if active is not None:
                product.active = active
            if category_id:
                product.category_id = category_id

            session.commit()
            return product.to_dict(), 200

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao atualizar produto: {e}")
            return {"erro": "Erro ao atualizar produto"}, 500
        finally:
            session.close()

    @classmethod
    def desactivate_product(cls, product_id):
        """Desativa um produto sem removê-lo"""
        session = Database.get_session()
        try:
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                return {"erro": "Produto não encontrado!"}, 404

            if not product.active:
                return {"erro": "O produto já está desativado!"}, 400

            product.active = False
            session.commit()
            return {"mensagem": f"Produto '{product.name}' foi desativado com sucesso."}, 200

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao desativar produto: {e}")
            return {"erro": "Erro ao desativar produto"}, 500
        finally:
            session.close()

    @classmethod
    def reactivate_product(cls, product_id):
        """Reativa um produto inativo"""
        session = Database.get_session()
        try:
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                return {"erro": "Produto não encontrado!"}, 404

            if product.active:
                return {"erro": "O produto já está ativo!"}, 400

            product.active = True
            session.commit()
            return {"mensagem": f"Produto '{product.name}' foi reativado com sucesso."}, 200

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao reativar produto: {e}")
            return {"erro": "Erro ao reativar produto"}, 500
        finally:
            session.close()
