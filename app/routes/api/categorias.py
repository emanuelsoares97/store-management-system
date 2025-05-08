from flask import Blueprint, jsonify, request
from app.services.CategoryService import CategoryService
from app.services.AuthService import AuthService
from app.util.logger_util import get_logger

category_bp = Blueprint("categories", __name__)
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

@category_bp.route("/nova", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def create_category():
    """Endpoint para criar uma nova categoria"""
    try:
        data = request.get_json()
        if not data:
            logger.warning(f"Tentativa de registar nova categoria sem dados.")
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        nome = data.get("nome")
        nova_categoria = CategoryService.criar_categoria(nome)
        logger.info(f"Nova categoria criada {nome}")
        return jsonify({"mensagem": "Categoria criada com sucesso!", "categoria": nova_categoria}), 201

    except ValueError as e:
        logger.error(f"Erro ao criar nova categoria, {str(e)}", exc_info=True)
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        logger.error(f"Erro ao criar categoria, {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao criar categoria."}), 500

@categoria_bp.route("/<int:categoria_id>/editar", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def update_category(categoria_id):
    """Endpoint para atualizar uma categoria"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        nome = data.get("nome")

        categoria_atualizada = CategoriaService.atualizar_categoria(categoria_id, nome)
        logger.info(f"Categoria atualizada: {nome}")
        return jsonify({"mensagem": "Categoria atualizada com sucesso!", "categoria": categoria_atualizada}), 200

    except ValueError as e:
        logger.error(f"Erro ao atualizar categoria, {str(e)}", exc_info=True)
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        logger.error(f"Erro ao atualizar categoria, {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao atualizar categoria."}), 500
