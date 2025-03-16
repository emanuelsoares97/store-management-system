from flask import Blueprint, request, jsonify, make_response
from services.utilizadoresmanager import UtilizadorService
from util.auth import AuthService 
from util.logger_util import get_logger

logger = get_logger("route_login")

login_bp = Blueprint("login", __name__)

@login_bp.route("/", methods=["POST"])
def login():
    """Autenticação de utilizador"""
    try:
        data = request.get_json()

        if not data or "email" not in data or "password" not in data:
            logger.warning("Tentativa de login sem credenciais fornecidas.")
            return make_response(jsonify({"erro": "Email e senha são obrigatórios!"}), 400)

        token = UtilizadorService.autenticar(data.get("email"), data.get("password"))

        if token:
            logger.info(f"Utilizador autenticado: {data.get('email')}")
            return jsonify({"token": token})

        logger.warning(f"Falha na autenticação para o email: {data.get('email')}")
        return make_response(jsonify({"erro": "Credenciais inválidas"}), 403)

    except Exception as e:
        logger.error(f"Erro inesperado no login: {str(e)}", exc_info=True)
        return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

@login_bp.route("/auth", methods=["GET"])
@AuthService.token_required
def auth():
    """Rota protegida que verifica se o token é válido"""
    try:
        logger.info("Token validado com sucesso!")
        return jsonify({"mensagem": "Token válido, utilizador autenticado!"})

    except Exception as e:
        logger.error(f"Erro ao validar token: {str(e)}", exc_info=True)
        return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

