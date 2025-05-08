import jwt
import uuid  # uuid para gerar identificadores únicos
from flask import request, jsonify, g 
from functools import wraps
from config import Config
from datetime import datetime, timezone, timedelta
from app.services.RevokedTokenService import TokenService
from app.util.logger_util import get_logger
from app.models.User import User 

logger = get_logger(__name__)

class AuthService:
    """Classe responsável por gerenciar autenticação JWT"""

    @staticmethod
    def generate_tokens(user):
        """Gera um access token (curto prazo) e um refresh token (longo prazo) com `jti`"""

        try:
            jti_access = str(uuid.uuid4())  # Identificador único para o access token
            jti_refresh = str(uuid.uuid4())  # Identificador único para o refresh token

            access_token = jwt.encode(
                {
                    "id": user.id, 
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "jti": jti_access,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
                },
                Config.SECRET_KEY,
                algorithm="HS256"
            )

            refresh_token = jwt.encode(
                {
                    "id": user.id,
                    "jti": jti_refresh,
                    "type": "refresh",
                    "exp": datetime.now(timezone.utc) + timedelta(days=7)
                },
                Config.SECRET_KEY,
                algorithm="HS256"
            )

            logger.info("Token gerado com sucesso.")
            return access_token, refresh_token

        except Exception as e:
            logger.error(f"Tentativa de gerar token, erro: {str(e)}")
            return {"mensagem": f"erro ao tentar gerar token: {str(e)}"}

    @staticmethod
    def validate_token(token):
        """Valida e decodifica um token JWT"""
        if not token:
            return None, "Token em falta"

        if "Bearer " in token:
            token = token.replace("Bearer ", "")

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])

            # Verifica se o token está na blacklist
            if TokenService.esta_na_blacklist(payload["jti"]):
                return None, "Token inválido. Faça login novamente."

            logger.debug("Token validado com sucesso.")
            return payload, None
        
        except jwt.ExpiredSignatureError:
            logger.warning("Tentativa de validar token expirado")
            return None, "Token expirado. Faça login novamente."
        
        except jwt.InvalidTokenError:
            logger.warning("Tentativa de validar token inválido.")
            return None, "Token inválido."

    @staticmethod
    def token_required(f):
        """Decorator that protects routes requiring a valid token"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            payload, error = AuthService.validate_token(token)

            if error:
                return jsonify({"error": error}), 401

            user_id = payload.get("id")
            user = User.query.get(user_id)

            if not user:
                return jsonify({"error": "User not found"}), 401

            g.current_user = user  # POO COM ORM
            g.token_jti = payload.get("jti")  # separa o jti para usar na validaçao de token na blacklist

            return f(*args, **kwargs)
        return decorated

    @staticmethod
    def role_required(*required_roles):
        """Decorator que protege rotas exigindo uma role específica"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                user_role = g.current_user.role
                user_name = g.current_user.name

                if user_role not in required_roles:
                    logger.warning(f"Unauthorized role access attempt by {user_name}")
                    return jsonify({"Alerta": f"Acesso negado, utilizador '{user_role}' sem permissão!"}), 403
                return f(*args, **kwargs)
            return decorated_function
        return decorator
