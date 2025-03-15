from flask import Blueprint, jsonify, request
from services.produtomanager import ProdutoService
from util.logger_util import get_logger

produto_bp = Blueprint("produto", __name__)
routelog = get_logger("produto_routes")

"""
    ROTAS PRODUTOS:
    - GET    /api/produto/           -> Listar todos os produtos
    - POST   /api/produto/novo       -> Adicionar um novo produto
    - DELETE /api/produto/<id>/remover  -> Remover um produto
    - PUT    /api/produto/<id>/editar   -> Editar um produto
"""

@produto_bp.route("/", methods=["GET"])
def lista_produtos():
    """Endpoint para listar todos os produtos"""
    try:
        routelog.info("Requisição GET para listar produtos.")
        produtos = ProdutoService.listar_produtos()
        return jsonify({"produtos": produtos}), 200
    except Exception as e:
        routelog.error(f"Erro ao listar produtos: {str(e)}")
        return jsonify({"erro": "Erro ao carregar produtos."}), 500


@produto_bp.route("/novo", methods=["POST"])
def adicionar_produto():
    """Endpoint para adicionar um novo produto"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        nome_produto = data.get("nome")
        preco = data.get("preco")

        if not nome_produto or preco is None:
            return jsonify({"erro": "Nome e preço são obrigatórios!"}), 400

        routelog.debug(f"Adicionando novo produto: {nome_produto}, Preço: {preco}")

        novo_produto = ProdutoService.adicionar_produto(nome_produto, preco)

        return jsonify({"mensagem": "Produto adicionado com sucesso!", "produto": novo_produto}), 201

    except ValueError as e:
        routelog.warning(f"Erro de validação: {str(e)}")
        return jsonify({"erro": str(e)}), 400

    except Exception as e:
        routelog.error(f"Erro inesperado ao adicionar produto: {str(e)}")
        return jsonify({"erro": "Erro ao adicionar produto."}), 500


@produto_bp.route("/<int:produto_id>/remover", methods=["DELETE"])
def remover_produto(produto_id):
    """Endpoint para remover um produto pelo ID"""
    try:
        routelog.info(f"Tentando remover produto ID: {produto_id}")
        resultado = ProdutoService.remover_produto(produto_id)
        return jsonify({"mensagem": resultado}), 200
    except ValueError as e:
        routelog.warning(f"Erro ao remover produto: {str(e)}")
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        routelog.error(f"Erro inesperado ao remover produto: {str(e)}")
        return jsonify({"erro": "Erro ao remover produto."}), 500


@produto_bp.route("/<int:produto_id>/editar", methods=["PUT"])
def atualizar_produto(produto_id):
    """Endpoint para atualizar um produto"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        novo_nome = data.get("nome")
        novo_preco = data.get("preco")

        routelog.debug(f"Atualizando produto ID: {produto_id}")

        resultado = ProdutoService.atualizar_dados(produto_id, novo_nome, novo_preco)

        return jsonify({"mensagem": "Produto atualizado com sucesso!", "produto": resultado}), 200

    except ValueError as e:
        routelog.warning(f"Erro ao atualizar produto: {str(e)}")
        return jsonify({"erro": str(e)}), 400

    except Exception as e:
        routelog.error(f"Erro inesperado ao atualizar produto: {str(e)}")
        return jsonify({"erro": "Erro ao atualizar produto."}), 500

