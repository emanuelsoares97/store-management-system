from app.models.Category import Category
from app.extensions import db
from app.utils.logger_util import get_logger
from app.utils.responses import success_response, error_response

logger = get_logger(__name__)

class CategoryService:
    @classmethod
    def list_categories(cls):
        categories = Category.query.all()
        result = []
        for c in categories:
            try:
                result.append(c.to_dict_basic())
            except Exception as e:
                logger.error(f"Erro ao serializar categoria {c.id}: {e}")
                continue
        return success_response({"categories": result})

    @classmethod
    def create_category(cls, name: str):
        if not name:
            return error_response("Nome da categoria é obrigatório!", 400)
        if Category.query.filter_by(name=name).first():
            return error_response("Já existe uma categoria com esse nome!", 400)
        try:
            new_cat = Category(name=name)
            db.session.add(new_cat)
            db.session.commit()
            db.session.refresh(new_cat)
            logger.info(f"Categoria criada: {new_cat.name}")
            return success_response({"category": new_cat.to_dict()}, "Categoria criada com sucesso!", 201)
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar categoria: {e}")
            return error_response("Erro ao criar categoria.", 500)

    @classmethod
    def update_category(cls, category_id, name):
        cat = db.session.get(Category, category_id)
        if not cat:
            return error_response("Categoria não encontrada!", 404)
        if not name:
            return error_response("Nome da categoria é obrigatório!", 400)
        try:
            cat.name = name
            db.session.commit()
            return success_response({"category": cat.to_dict()}, "Categoria atualizada com sucesso!")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar categoria: {e}")
            return error_response("Erro ao atualizar categoria.", 500)
