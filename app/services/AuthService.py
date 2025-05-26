import jwt
import uuid
from flask import request, jsonify, g
from functools import wraps
from datetime import datetime, timezone, timedelta

from config import Config
from app.extensions import db
from app.models.User import User
from app.services.RevokedTokenService import TokenService
from app.utils.logger_util import get_logger

logger = get_logger(__name__)

class AuthService:
    """Classe responsável por gerenciar autenticação JWT"""

    @staticmethod
    def generate_tokens(user):
        """Gera access e refresh tokens com identificadores únicos (jti)"""
        jti_access = str(uuid.uuid4())
        jti_refresh = str(uuid.uuid4())

        access_payload = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "jti": jti_access,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
        }
        refresh_payload = {
            "id": user.id,
            "jti": jti_refresh,
            "type": "refresh",
            "exp": datetime.now(timezone.utc) + timedelta(days=7)
        }

        access_token = jwt.encode(access_payload, Config.SECRET_KEY, algorithm="HS256")
        refresh_token = jwt.encode(refresh_payload, Config.SECRET_KEY, algorithm="HS256")

        logger.info("Tokens gerados com sucesso.")
        return access_token, refresh_token

    @staticmethod
    def validate_token(token):
        """Valida e decodifica um JWT, checando blacklist e expiração"""
        if not token:
            return None, "Token em falta"

        if token.startswith("Bearer "):
            token = token.split(" ", 1)[1]

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            if TokenService.in_blacklist(payload.get("jti")):
                return None, "Token inválido. Faça login novamente."
            return payload, None

        except jwt.ExpiredSignatureError:
            logger.warning("Tentativa de validar token expirado.")
            return None, "Token expirado. Faça login novamente."

        except jwt.InvalidTokenError:
            logger.warning("Tentativa de validar token inválido.")
            return None, "Token inválido."

    @staticmethod
    def token_required(f):
        """Decorator para rotas que exigem um token válido"""
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            payload, error = AuthService.validate_token(auth_header)
            if error:
                return jsonify({"Alerta": error}), 401

            user = db.session.get(User, payload.get("id"))
            if not user:
                return jsonify({"Alerta": "Utilizador não encontrado"}), 401

            g.current_user = user
            g.token_jti = payload.get("jti")
            return f(*args, **kwargs)
        return decorated

    @staticmethod
    def role_required(*required_roles):
        """Decorator para rotas que exigem uma role específica"""
        def wrapper(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                role = getattr(g.current_user, "role", None)
                if role not in required_roles:
                    msg = f"Acesso negado, utilizador '{role}' sem permissão!"
                    return jsonify({"Alerta": msg}), 403
                return f(*args, **kwargs)
            return decorated
        return wrapper
