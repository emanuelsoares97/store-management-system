from flask import Blueprint, jsonify, request
from app.services.CategoryService import CategoryService
from app.services.AuthService import AuthService
from app.utils.logger_util import get_logger

category_bp = Blueprint("category", __name__)
logger = get_logger(__name__)

@category_bp.route("/list", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def list_categories():
    """Endpoint para listar todas as categorias"""
    try:

        return CategoryService.list_categories()
    
    except Exception as e:
        logger.error(f"Erro ao listar categorias: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao carregar categorias."}), 500

@category_bp.route("/new", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def create_category():
    """Endpoint para criar uma nova categoria"""
    try:
        # Tenta obter JSON do request, se for None ou inválido, usa dict vazio
        data = request.get_json(silent=True) or {}

        name = data.get("name")
        logger.info(f"Nova categoria criada {name}")
        return CategoryService.create_category(name)

    except Exception as e:
        logger.error(f"Erro ao criar categoria, {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao criar categoria."}), 500

@category_bp.route("/<int:category_id>/update", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def update_category(category_id):
    """Endpoint para atualizar uma categoria"""
    try:
        # Tenta obter JSON do request, se for None ou inválido, usa dict vazio
        data = request.get_json(silent=True) or {}

        name = data.get("name")

        logger.info(f"Categoria atualizada: {name}")
        return CategoryService.update_category(category_id, name)

    except Exception as e:
        logger.error(f"Erro ao atualizar categoria, {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao atualizar categoria."}), 500
