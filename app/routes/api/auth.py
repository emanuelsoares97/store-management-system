from flask import Blueprint, request, jsonify, make_response, g
from app.services.UserService import UserService
from app.services.AuthService import AuthService 
from app.util.logger_util import get_logger
from app.services.RevokedTokenService import TokenService
import re
import jwt
from config import Config
from collections import namedtuple

logger = get_logger(__name__)

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def home():
    return jsonify({"status": "alive"}), 200


@auth_bp.route("/login", methods=["POST"])
def login():
    """Autenticação de utilizador"""
    try:
        logger.debug("Rota /api/auth/login chamada.")

        if not request.is_json:
            logger.info("Formato de envio incorreto, não foi JSON")
            return jsonify({"erro": "Formato inválido, envie um JSON"}), 400

        data = request.get_json()
        logger.info(f"Dados recebidos: {data}")

        if not data or "email" not in data or "password" not in data:
            logger.warning("Tentativa de login sem credenciais fornecidas.")
            return jsonify({"erro": "Email e senha são obrigatórios!"}), 400

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, data["email"]):
            logger.warning("Tentativa de login com email inválido.")
            return jsonify({"erro": "Email inválido"}), 400

        user = UserService.auth_user(data.get("email"), data.get("password")) 

        if not user:
            logger.warning(f"Falha na autenticação para o email: {data.get('email')}")
            return jsonify({"erro": "Credenciais inválidas"}), 403

        if not user.active:
            logger.warning(f"Tentativa de login de utilizador desativado: {user.email}")
            return jsonify({"erro": "Conta desativada. Entre em contato com o suporte."}), 403

        access_token, refresh_token = AuthService.generate_tokens(user)

        logger.info(f"Utilizador autenticado: {user.email}")
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "utilizador": {
                "id": user.id,
                "email": user.email,
                "role": user.role
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
@AuthService.token_required
def logout():
    """Revoga o access token do utilizador"""
    try:
        TokenService.add_token_to_blacklist(g.token_jti)

        logger.info("Logout com sucesso")
        return jsonify({"mensagem": "Logout bem-sucedido!"}), 200

    except Exception as e:
        logger.error(f"Erro ao efetuar logout: {str(e)}", exc_info=True)
        return jsonify({"mensagem": "Token em falta para logout"}), 401


@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    """Renova o access token usando o refresh token"""
    token = request.headers.get("Authorization") #recebe o token 

    if not token:
        logger.warning("Refresh token em falta")
        return jsonify({"erro": "Refresh token é obrigatório!"}), 401

    token = token.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"]) #validaçao do token

        if payload.get("type") != "refresh":
            return jsonify({"erro": "Token inválido para refresh."}), 403

        UserTuple = namedtuple("User", ["id", "name", "email", "role"])
        user_obj = UserTuple(id=payload["id"], name=payload.get("name", ""), email="", role="")


        new_access_token, _ = AuthService.generate_tokens(user_obj) #token renovado

        return jsonify({"access_token": new_access_token}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Refresh token expirado. Faça login novamente!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Refresh token inválido!"}), 401
