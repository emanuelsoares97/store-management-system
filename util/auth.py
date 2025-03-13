import jwt
from flask import request, jsonify
from functools import wraps
from config import SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")  # Obtém o token do header

        if not token:
            return jsonify({"Alerta": "Token em falta"}), 401

        # Remover o prefixo "Bearer " caso esteja presente
        if "Bearer " in token:
            token = token.replace("Bearer ", "")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])  # Decodifica o JWT
            
        except jwt.ExpiredSignatureError:
            return jsonify({"Alerta": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"Alerta": "Token inválido"}), 401

        return f(*args, **kwargs)  # Continua para a função original

    return decorated
