from flask import Blueprint, request, jsonify
from services.utilizadoresmanager import UtilizadorService
from util.auth import AuthService

utilizador_bp = Blueprint("utilizador", __name__)

@utilizador_bp.route("/", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")  #Apenas admins podem listar utilizadores
def listar_utilizadores():
    """Lista todos os utilizadores"""
    utilizadores = UtilizadorService.listar_utilizadores()
    return jsonify(utilizadores), 200

@utilizador_bp.route("/novo", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def criar_utilizador():
    """Cria um novo utilizador"""
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    password = data.get("password")

    resposta, status = UtilizadorService.criar_utilizador(nome, email, password)
    return jsonify(resposta), status

@utilizador_bp.route("/<int:utilizador_id>/editar", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin")  #so os admin podem modificar
def atualizar_utilizador(utilizador_id):
    """Endpoint para atualizar um utilizador"""
    data = request.get_json()
    
    if not data:
        return jsonify({"erro": "Nenhum dado enviado!"}), 400

    # garantir que é um admin a modificar os dados
    user_role = request.user_role  

    resultado = UtilizadorService.atualizar_utilizador(
        utilizador_id,
        nome=data.get("nome"),
        email=data.get("email"),
        password=data.get("password"),
        role=data.get("role"),
    )

    return jsonify(resultado)


@utilizador_bp.route("/<int:utilizador_id>/remover", methods=["DELETE"])
@AuthService.token_required
@AuthService.role_required("admin")
def remover_utilizador(utilizador_id):
    """Remove um utilizador"""
    resposta, status = UtilizadorService.remover_utilizador(utilizador_id)
    return jsonify(resposta), status
