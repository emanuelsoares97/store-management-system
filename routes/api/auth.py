from flask import Blueprint, request, jsonify, make_response, g
from services.utilizadoresmanager import UtilizadorService
from util.auth import AuthService 
from util.logger_util import get_logger
from services.tokenrevogadomanager import TokenService

logger = get_logger("route_auth")

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    """Autenticação de utilizador"""
    try:
        data = request.get_json()

        if not data or "email" not in data or "password" not in data:
            logger.warning("Tentativa de login sem credenciais fornecidas.")
            return jsonify({"erro": "Email e senha são obrigatórios!"}), 400

        utilizador = UtilizadorService.autenticar(data.get("email"), data.get("password"))

        if not utilizador:
            logger.warning(f"Falha na autenticação para o email: {data.get('email')}")
            return jsonify({"erro": "Credenciais inválidas"}), 403

        access_token, refresh_token = AuthService.gerar_tokens(utilizador)

        logger.info(f"Utilizador autenticado: {utilizador.email}")
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "utilizador": {
                "id": utilizador.id,
                "email": utilizador.email,
                "role": utilizador.role
            }
        })

    except Exception as e:
        logger.error(f"Erro inesperado no login: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro interno no servidor"}), 500



@auth_bp.route("/auth", methods=["GET"])
@AuthService.token_required
def auth():
    """Rota protegida que verifica se o token é válido"""
    try:
        logger.info("Token validado com sucesso!")
        return jsonify({"mensagem": "Token válido, utilizador autenticado!"})

    except Exception as e:
        logger.error(f"Erro ao validar token: {str(e)}", exc_info=True)
        return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)
    
@auth_bp.route("/logout", methods=["POST"])
@AuthService.token_required  # Já valida o token automaticamente
def logout():
    """Revoga o access token do utilizador"""
    token = request.headers.get("Authorization").replace("Bearer ", "")

    # O token já foi validado pelo @AuthService.token_required, então podemos pegar o JTI
    TokenService.adicionar_token_na_blacklist(g.current_user["jti"])

    return jsonify({"mensagem": "Logout bem-sucedido!"}), 200





