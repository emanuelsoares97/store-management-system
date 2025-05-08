from app.models.Category import Category
from app.database import Database
from app.util.logger_util import get_logger

class CategoryService:
    """Gerencia as categorias no banco de dados"""

    logger = get_logger(__name__)

    @classmethod
    def list_categories(cls):
        """Retorna a lista de todas as categorias"""
        session = Database.get_session()
        try:
            categories = session.query(Category).all()
            return {"categorias": [c.to_dict() for c in categories]}, 200
        finally:
            session.close()

    @classmethod
    def create_category(cls, name):
        """Cria uma nova categoria"""
        session = Database.get_session()
        try:
            if not name:
                return {"erro": "Nome da categoria é obrigatório!"}, 400

            existing = session.query(Category).filter_by(name=name).first()
            if existing:
                return {"erro": "Já existe uma categoria com esse nome!"}, 400

            new_category = Category(name=name)
            session.add(new_category)
            session.commit()
            session.refresh(new_category)

            cls.logger.info(f"Categoria criada: {new_category.name}")
            return {
                "mensagem": "Categoria criada com sucesso!",
                "categoria": new_category.to_dict()
            }, 201

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao criar categoria: {e}")
            return {"erro": "Erro ao criar categoria."}, 500
        finally:
            session.close()

    @classmethod
    def update_category(cls, category_id, name):
        """Atualiza o nome de uma categoria"""
        session = Database.get_session()
        try:
            category = session.query(Category).filter_by(id=category_id).first()
            if not category:
                return {"erro": "Categoria não encontrada!"}, 404

            category.name = name
            session.commit()

            return {
                "mensagem": "Categoria atualizada com sucesso!",
                "categoria": category.to_dict()
            }, 200

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao atualizar categoria: {e}")
            return {"erro": "Erro ao atualizar categoria."}, 500
        finally:
            session.close()
