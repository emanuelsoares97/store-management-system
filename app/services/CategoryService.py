from app.models.Category import Category
from app.extensions import db
from app.util.logger_util import get_logger

logger = get_logger(__name__)

class CategoryService:
    """Gerencia as categorias dos produtos"""

    @classmethod
    def list_categories(cls):
        """retorna a lista das categorias"""
        categories = Category.query.all()
        return {"categories": [c.to_dict() for c in categories]}, 200

    @classmethod
    def create_category(cls, name: str):
        """Criar nova categoria"""
        if not name:
            return {"error": "Nome da categoria é obrigatório!"}, 400

        if Category.query.filter_by(name=name).first():
            return {"error": "Já existe uma categoria com esse nome!"}, 400

        try:
            new_cat = Category(name=name)
            db.session.add(new_cat)
            db.session.commit()
            db.session.refresh(new_cat)
            logger.info(f"Categoria criada: {new_cat.name}")
            return {
                "message": "Categoria criada com sucesso!",
                "category": new_cat.to_dict()
            }, 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar categoria: {e}")
            return {"error": "Erro ao criar categoria."}, 500

    @classmethod
    def update_category(cls, category_id: int, name: str):
        """editar categoria"""
        cat = Category.query.get(category_id)
        if not cat:
            return {"error": "Categoria não encontrada!"}, 404

        if not name:
            return {"error": "Nome da categoria é obrigatório!"}, 400

        try:
            cat.name = name
            db.session.commit()
            return {
                "message": "Categoria atualizada com sucesso!",
                "category": cat.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar categoria: {e}")
            return {"error": "Erro ao atualizar categoria."}, 500
