from flask import Blueprint, request, jsonify, make_response, g
from services.utilizadoresmanager import UtilizadorService
from services.authmanager import AuthService 
from util.logger_util import get_logger
from services.tokenrevogadomanager import TokenService
import re
import jwt
from config import Config
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
            return jsonify({"erro": "Formato inválido, envie um JSON"}), 400
        
        data = request.get_json()

        logger.info(f"Dados recebidos: {data}")

        if not data or "email" not in data or "password" not in data:
            logger.warning("Tentativa de login sem credenciais fornecidas.")
            return jsonify({"erro": "Email e senha são obrigatórios!"}), 400


        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, data["email"]):
            logger.warning("Tenativa de login de email envalido.")
            return jsonify({"erro": "Email inválido"}), 400
        
        
        
        utilizador = UtilizadorService.autenticar(data.get("email"), data.get("password")) 
        
        if not utilizador:
            logger.warning(f"Falha na autenticação para o email: {data.get('email')}")
            return jsonify({"erro": "Credenciais inválidas"}), 403
        
        if not utilizador.ativo:  # Garante que a conta está ativa
            logger.warning(f"Tentativa de login de utilizador desativo: {utilizador.email}")
            return jsonify({"erro": "Conta desativada. Entre em contato com o suporte."}), 403 

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
    try:
        token = request.headers.get("Authorization").replace("Bearer ", "")

        # O token já foi validado pelo @AuthService.token_required, então podemos pegar o JTI
        TokenService.adicionar_token_na_blacklist(g.current_user["jti"])
        
        logger.info("Logout com sucesso")
        return jsonify({"mensagem": "Logout bem-sucedido!"}), 200
    
    except Exception as e:
        logger.error(f"Erro ao validar token: {str(e)}", exc_info=True)
        return jsonify({"mensagem": "Token em falta para logout"}), 401


@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    """Renova o access token usando o refresh token"""
    token = request.headers.get("Authorization")  # Pega o token enviado pelo cliente

    if not token:
        logger.warning
        return jsonify({"erro": "Refresh token é obrigatório!"}), 401

    token = token.replace("Bearer ", "")  # Remove "Bearer " se estiver presente

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        
        Utilizador = namedtuple("Utilizador", ["id", "nome", "email", "role"])
        utilizador_obj = Utilizador(id=payload["id"], nome=payload.get("nome", ""), email="", role="")

        novo_access_token, _ = AuthService.gerar_tokens(utilizador_obj)

        return jsonify({"access_token": novo_access_token}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Refresh token expirado. Faça login novamente!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Refresh token inválido!"}), 401