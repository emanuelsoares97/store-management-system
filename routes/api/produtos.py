from flask import Blueprint, jsonify, request
from services.produtomanager import ProdutoService
from util.logger_util import get_logger
from util.auth import AuthService

produto_bp = Blueprint("produto", __name__)
routelog = get_logger("produto_routes")

"""
    ROTAS PRODUTOS:
    - GET    /api/produto/             -> Listar todos os produtos ativos
    - POST   /api/produto/novo         -> Criar um novo produto
    - PUT    /api/produto/<id>/editar  -> Editar um produto
    - PATCH  /api/produto/<id>/desativar -> Desativar um produto
    - PATCH  /api/produto/<id>/reativar -> Reativar um produto
"""

@produto_bp.route("/", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "estoque", "user") 
def listar_produtos():
    """Endpoint para listar todos os produtos ativos"""
    try:
        routelog.info("Listando produtos ativos.")
        produtos = ProdutoService.listar_produtos()
        return jsonify({"produtos": produtos}), 200
    except Exception as e:
        routelog.error(f"Erro ao listar produtos: {str(e)}")
        return jsonify({"erro": "Erro ao carregar produtos."}), 500


@produto_bp.route("/novo", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def criar_produto():
    """Endpoint para criar um novo produto"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        nome = data.get("nome")
        preco = data.get("preco")
        estoque = data.get("estoque")
        categoria_id = data.get("categoria_id")

        novo_produto = ProdutoService.criar_produto(nome, preco, estoque, categoria_id)
        return jsonify({"mensagem": "Produto criado com sucesso!", "produto": novo_produto}), 201

    except ValueError as e:
        routelog.warning(f"Erro de validação: {str(e)}")
        return jsonify({"erro": str(e)}), 400

    except Exception as e:
        routelog.error(f"Erro inesperado ao criar produto: {str(e)}")
        return jsonify({"erro": "Erro ao criar produto."}), 500


@produto_bp.route("/<int:produto_id>/editar", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def atualizar_produto(produto_id):
    """Endpoint para atualizar um produto"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        resultado = ProdutoService.atualizar_dados(
            produto_id,
            nome=data.get("nome"),
            preco=data.get("preco"),
            estoque=data.get("estoque"),
            ativo=data.get("ativo"),
            categoria_id=data.get("categoria_id")
        )

        return jsonify({"mensagem": "Produto atualizado com sucesso!", "produto": resultado}), 200

    except ValueError as e:
        routelog.warning(f"Erro ao atualizar produto: {str(e)}")
        return jsonify({"erro": str(e)}), 400

    except Exception as e:
        routelog.error(f"Erro inesperado ao atualizar produto: {str(e)}")
        return jsonify({"erro": "Erro ao atualizar produto."}), 500


@produto_bp.route("/<int:produto_id>/reativar", methods=["PATCH"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def reativar_produto(produto_id):
    """Endpoint para reativar um produto"""
    try:
        resultado = ProdutoService.reativar_produto(produto_id)
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao reativar produto."}), 500

@produto_bp.route("/<int:produto_id>/desativar", methods=["PATCH"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def desativar_produto(produto_id):
    """Endpoint para desativar um produto"""
    try:
        resultado = ProdutoService.desativar_produto(produto_id)
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao desativar produto."}), 500
