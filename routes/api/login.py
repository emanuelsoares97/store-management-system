from flask import jsonify, request, render_template, make_response, session, Blueprint

from data.json_manager import carregar_lista
from config import DEBUG, SECRET_KEY
from util.auth import token_required
from util.logger_util import get_logger
import jwt
from datetime import datetime, timedelta


login_bp=Blueprint("login", __name__)

routelog = get_logger("login_routes")




"""
    ROTA LOGIN:
    - /login (POST) - Envia dados para o servidor e é feita a validação   - /auth (GET)   - Recebe os dados enviados pelo cliente caso seja autorizado faz o login

"""


@login_bp.route("/login", methods=["POST"])
def login():
    """Autenticação de utilizador """
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # Simulação de verificação de credenciais
    if username == "admin" and password == "123456":
        session["logged_in"] = True
        token = jwt.encode(
            {
                "user": username,
                "exp": datetime.utcnow() + timedelta(seconds=120)  # Token expira em 2 minutos
            }, 
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"token": token})
    else:
        return make_response(jsonify({"erro": "Credenciais inválidas"}), 403)

@login_bp.route("/auth", methods=["GET"])
@token_required
def auth():
    """retorna 'sucesso' se for valido"""
    return jsonify({"mensagem": "JWT verificado, bem-vindo!"})