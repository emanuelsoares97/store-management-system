import jwt
from flask import request, jsonify
from functools import wraps
from config import Config
from datetime import datetime, timedelta

class AuthService:
    """Classe responsável por gerenciar autenticação JWT"""

    @staticmethod
    def gerar_token(utilizador):
        """Gera um token JWT com a role do utilizador"""
        return jwt.encode(
            {
                "email": utilizador["email"],
                "role": utilizador["role"],
                "exp": datetime.utcnow() + timedelta(hours=1)
            },
            Config.SECRET_KEY,
            algorithm="HS256"
        )

    @staticmethod
    def validar_token(token):
        """Valida e decodifica um token JWT"""
        if not token:
            return None, "Token em falta"

        if "Bearer " in token:
            token = token.replace("Bearer ", "")

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            return payload, None  # Retorna os dados decodificados
        except jwt.ExpiredSignatureError:
            return None, "Token expirado"
        except jwt.InvalidTokenError:
            return None, "Token inválido"

    @staticmethod
    def token_required(f):
        """Decorator que protege rotas exigindo um token válido"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            payload, error = AuthService.validar_token(token)

            if error:
                return jsonify({"Alerta": error}), 401

            request.user_role = payload["role"]  # Define a role do utilizador na request
            return f(*args, **kwargs)

        return decorated

    @staticmethod
    def role_required(*required_roles):
        """Decorator que protege rotas exigindo uma role específica"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                user_role = request.user_role  # Pegamos a role da request

                if user_role not in required_roles:
                    return jsonify({"Alerta": f"Acesso negado, utilizador '{user_role}' sem permissão!"}), 403
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator
