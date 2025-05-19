from flask import Blueprint, jsonify, request
from app.services.CategoryService import CategoryService
from app.services.AuthService import AuthService
from app.util.logger_util import get_logger

category_bp = Blueprint("category", __name__)
logger = get_logger(__name__)

@category_bp.route("/list", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def list_categories():
    """Endpoint para listar todas as categorias"""
    try:
        categories, status = CategoryService.list_categories()
        return jsonify(categories), status
    except Exception as e:
        logger.error(f"Erro ao listar categorias: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao carregar categorias."}), 500

@category_bp.route("/new", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def create_category():
    """Endpoint para criar uma nova categoria"""
    try:
        data = request.get_json()
        if not data:
            logger.warning(f"Tentativa de registar nova categoria sem dados.")
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        name = data.get("name")
        new_category, status = CategoryService.create_category(name)
        logger.info(f"Nova categoria criada {name}")
        return jsonify(new_category), status

    except ValueError as e:
        logger.error(f"Erro ao criar nova categoria, {str(e)}", exc_info=True)
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        logger.error(f"Erro ao criar categoria, {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao criar categoria."}), 500

@category_bp.route("/<int:category_id>/update", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def update_category(category_id):
    """Endpoint para atualizar uma categoria"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        name = data.get("name")

        update_category, status = CategoryService.update_category(category_id, name)
        logger.info(f"Categoria atualizada: {name}")
        return jsonify(update_category), status

    except ValueError as e:
        logger.error(f"Erro ao atualizar categoria, {str(e)}", exc_info=True)
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        logger.error(f"Erro ao atualizar categoria, {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao atualizar categoria."}), 500
