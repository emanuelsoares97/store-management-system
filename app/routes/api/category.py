from flask import Blueprint, request
from app.services.CategoryService import CategoryService
from app.services.AuthService import AuthService
from app.utils.logger_util import get_logger
from app.utils.responses import success_response, error_response

category_bp = Blueprint("category", __name__)
logger = get_logger(__name__)

@category_bp.route("/list", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def list_categories():
    """Endpoint para listar todas as categorias"""
    try:
        categorias = CategoryService.list_categories()
        return categorias

    except Exception as e:
        logger.error(f"Erro ao listar categorias: {str(e)}", exc_info=True)
        return error_response("Erro ao carregar categorias.", 500)


@category_bp.route("/new", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def create_category():
    """Endpoint para criar uma nova categoria"""
    try:
        data = request.get_json(silent=True) or {}
        name = data.get("name")

        if not name:
            return error_response("O nome da categoria é obrigatório.", 400)

        nova_categoria = CategoryService.create_category(name)
        logger.info(f"Nova categoria criada: {nova_categoria}")
        return nova_categoria

    except Exception as e:
        logger.error(f"Erro ao criar categoria: {str(e)}", exc_info=True)
        return error_response("Erro ao criar categoria.", 500)


@category_bp.route("/<int:category_id>/update", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def update_category(category_id):
    """Endpoint para atualizar uma categoria"""
    try:
        data = request.get_json(silent=True) or {}
        name = data.get("name")

        if not name:
            return error_response("O novo nome da categoria é obrigatório.", 400)

        categoria_atualizada = CategoryService.update_category(category_id, name)
        logger.info(f"Categoria atualizada: {categoria_atualizada}")
        return categoria_atualizada

    except Exception as e:
        logger.error(f"Erro ao atualizar categoria: {str(e)}", exc_info=True)
        return error_response("Erro ao atualizar categoria.", 500)
