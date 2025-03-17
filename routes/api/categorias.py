from flask import Blueprint, jsonify, request
from services.categoriamanager import CategoriaService
from util.auth import AuthService
from util.logger_util import get_logger

categoria_bp = Blueprint("categoria", __name__)
routelog = get_logger("categoria_routes")

@categoria_bp.route("/", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def listar_categorias():
    """Endpoint para listar todas as categorias"""
    try:
        categorias = CategoriaService.listar_categorias()
        return jsonify({"categorias": categorias}), 200
    except Exception as e:
        routelog.error(f"Erro ao listar categorias: {str(e)}")
        return jsonify({"erro": "Erro ao carregar categorias."}), 500

@categoria_bp.route("/nova", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def criar_categoria():
    """Endpoint para criar uma nova categoria"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        nome = data.get("nome")
        nova_categoria = CategoriaService.criar_categoria(nome)
        return jsonify({"mensagem": "Categoria criada com sucesso!", "categoria": nova_categoria}), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao criar categoria."}), 500

@categoria_bp.route("/<int:categoria_id>/editar", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def atualizar_categoria(categoria_id):
    """Endpoint para atualizar uma categoria"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        nome = data.get("nome")

        categoria_atualizada = CategoriaService.atualizar_categoria(categoria_id, nome)
        return jsonify({"mensagem": "Categoria atualizada com sucesso!", "categoria": categoria_atualizada}), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao atualizar categoria."}), 500
