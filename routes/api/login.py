from flask import Blueprint, request, jsonify, make_response
from services.utilizadoresmanager import UtilizadorService
from util.auth import AuthService 

login_bp = Blueprint("login", __name__)

@login_bp.route("/", methods=["POST"])
def login():
    """Autenticação de utilizador"""
    data = request.get_json()
    token = UtilizadorService.autenticar(data.get("email"), data.get("password"))

    if token:
        return jsonify({"token": token})

    return make_response(jsonify({"erro": "Credenciais inválidas"}), 403)

@login_bp.route("/auth", methods=["GET"])
@AuthService.token_required
def auth():
    """Rota protegida que verifica se o token é válido"""
    return jsonify({"mensagem": "Token válido, utilizador autenticado!"})
