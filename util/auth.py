import jwt
import uuid  #uuid para gerar identificadores únicos
from flask import request, jsonify, g 
from functools import wraps
from config import Config
from datetime import datetime, timezone, timedelta
from services.tokenrevogadomanager import TokenService

class AuthService:
    """Classe responsável por gerenciar autenticação JWT"""

    @staticmethod
    def gerar_tokens(utilizador):
        """Gera um access token (curto prazo) e um refresh token (longo prazo) com `jti`"""
        jti_access = str(uuid.uuid4())  # Identificador único para o access token
        jti_refresh = str(uuid.uuid4())  # Identificador único para o refresh token

        access_token = jwt.encode(
            {
                "id": utilizador.id,  # ✅ Agora acessamos como objeto
                "email": utilizador.email,
                "role": utilizador.role,
                "jti": jti_access,  # `jti` ao access token
                "exp": datetime.now(timezone.utc) + timedelta(minutes=15)  # Expira em 15 min
            },
            Config.SECRET_KEY,
            algorithm="HS256"
        )

        refresh_token = jwt.encode(
            {
                "id": utilizador.id,  # ✅ Agora acessamos como objeto
                "jti": jti_refresh,  # Adicionamos `jti` ao refresh token
                "exp": datetime.now(timezone.utc) + timedelta(days=7)  # Expira em 7 dias
            },
            Config.SECRET_KEY,
            algorithm="HS256"
        )

        return access_token, refresh_token




    @staticmethod
    def validar_token(token):
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

            return payload, None
        except jwt.ExpiredSignatureError:
            return None, "Token expirado. Faça login novamente."
        except jwt.InvalidTokenError:
            return None, "Token inválido."


    @staticmethod
    def token_required(f):
        """Decorator que protege rotas exigindo um token válido"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            payload, error = AuthService.validar_token(token)

            if error:
                return jsonify({"Alerta": error}), 401

            
            g.current_user = {
                "email": payload["email"],
                "role": payload["role"],
                "jti": payload["jti"]  # identificador único do token
            }

            return f(*args, **kwargs)

        return decorated


    @staticmethod
    def role_required(*required_roles):
        """Decorator que protege rotas exigindo uma role específica"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                user_role = g.current_user["role"]

                if user_role not in required_roles:
                    return jsonify({"Alerta": f"Acesso negado, utilizador '{user_role}' sem permissão!"}), 403
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator
