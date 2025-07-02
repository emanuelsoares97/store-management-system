from flask import Blueprint, request, g
from app.services.UserService import UserService
from app.services.AuthService import AuthService 
from app.utils.logger_util import get_logger
from app.services.RevokedTokenService import TokenService
from app.utils.responses import success_response, error_response
from config import Config
import re
import jwt
from collections import namedtuple

logger = get_logger(__name__)

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    """Autenticação de utilizador"""
    try:
        logger.debug("Rota /api/auth/login chamada.")

        if not request.is_json:
            logger.info("Formato de envio incorreto, não foi JSON")
            return error_response("Formato inválido, envie um JSON", 400)

        data = request.get_json()
        logger.info(f"Dados recebidos: {data}")

        if not data or "email" not in data or "password" not in data:
            logger.warning("Tentativa de login sem credenciais fornecidas.")
            return error_response("Email e password são obrigatórios!", 400)

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, data["email"]):
            logger.warning("Tentativa de login com email inválido.")
            return error_response("Email inválido", 400)

        user = UserService.auth_user(data.get("email"), data.get("password")) 

        if not user:
            logger.warning(f"Falha na autenticação para o email: {data.get('email')}")
            return error_response("Credenciais inválidas", 403)

        if not user.active:
            logger.warning(f"Tentativa de login de utilizador desativado: {user.email}")
            return error_response("Conta desativada. Entre em contato com o suporte.", 403)

        access_token, refresh_token = AuthService.generate_tokens(user)

        logger.info(f"Utilizador autenticado: {user.email}")
        return success_response(
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role
                }
            }
        )

    except Exception as e:
        logger.error(f"Erro inesperado no login: {str(e)}", exc_info=True)
        return error_response("Erro interno no servidor", 500)


@auth_bp.route("/auth", methods=["GET"])
@AuthService.token_required
def auth():
    """Rota protegida que verifica se o token é válido"""
    try:
        logger.info("Token validado com sucesso!")
        return success_response(message="Token válido, utilizador autenticado!")
    except Exception as e:
        logger.error(f"Erro ao validar token: {str(e)}", exc_info=True)
        return error_response("Token inválido.", 401)


@auth_bp.route("/logout", methods=["POST"])
@AuthService.token_required
def logout():
    """Revoga o access token do utilizador"""
    try:
        TokenService.add_to_blacklist(g.token_jti)
        logger.info("Logout com sucesso")
        return success_response(message="Logout bem-sucedido!")
    except Exception as e:
        logger.error(f"Erro ao efetuar logout: {str(e)}", exc_info=True)
        return error_response("Token em falta para logout", 401)


@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    """Renova o access token usando o refresh token"""
    token = request.headers.get("Authorization") 

    if not token:
        logger.warning("Refresh token em falta")
        return error_response("Refresh token é obrigatório!", 401)

    token = token.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])

        if payload.get("type") != "refresh":
            return error_response("Token inválido para refresh.", 403)

        UserTuple = namedtuple("User", ["id", "name", "email", "role"])
        user_obj = UserTuple(id=payload["id"], name=payload.get("name", ""), email="", role="")

        new_access_token, _ = AuthService.generate_tokens(user_obj)

        return success_response(data={"access_token": new_access_token})

    except jwt.ExpiredSignatureError:
        return error_response("Refresh token expirado. Faça login novamente!", 401)
    except jwt.InvalidTokenError:
        return error_response("Refresh token inválido!", 401)
