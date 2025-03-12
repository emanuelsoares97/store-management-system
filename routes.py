from flask import jsonify, request
from services.produtomanager import ProdutoManager
from gestãoprodutos.tratamentolista import carregar_lista
from config import DEBUG
from util.logger_util import get_logger

applog = get_logger("applog")
manager = ProdutoManager()
produtos = carregar_lista()

def init_routes(app):
    @app.route("/")
    def homepage():
        return "Como familia", 201

    @app.route("/produtos", methods=["GET"])
    def lista_produtos():
        try:
            return jsonify(produtos), 200
        except Exception as e:
            return jsonify({"erro": f"Erro ao carregar produtos: {str(e)}"}), 500

    @app.route("/produto", methods=["POST"])
    def adicionar_produto():
        try:
            data = request.get_json()
            nome_produto = data["nome"]
            preco = float(data["preco"])

            manager.adicionar_produto(nome_produto, preco)

            return jsonify({"mensagem": "Produto adicionado com sucesso!"}), 201
        except Exception as e:
            return jsonify({"erro": f"Erro ao adicionar produto: {str(e)}"}), 400

    @app.route("/produto/<int:id>", methods=["DELETE"])
    def remover_produto(id):
        produtos_antes = len(manager.listaprodutos) 
        
        manager.remover_produto_id(id)
        
        if len(manager.listaprodutos) < produtos_antes:
            return jsonify({"mensagem": "Produto removido com sucesso!"}), 200
        else:
            return jsonify({"erro": "Produto não encontrado."}), 404

    @app.route("/produto/<int:id>", methods=["PUT"])
    def atualizar_produto(id):
        try:
            data = request.get_json()
            novo_nome = data.get("nome")
            novo_preco = data.get("preco")

            atualizado = manager.atualizar_produto(id, novo_nome, novo_preco)

            if not atualizado:
                return jsonify({"erro": "Produto não encontrado."}), 404

            return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 200

        except Exception as e:
            return jsonify({"erro": f"Erro ao atualizar produto: {str(e)}"}), 400
