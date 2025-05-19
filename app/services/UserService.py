from flask import g
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.User import User
from app.util.logger_util import get_logger
from app.util.validate_email_phone import validate_email

logger = get_logger(__name__)

class UserService:
    """Gerencia autenticação e operações com utilizadores"""

    @classmethod
    def auth_user(cls, email, password):
        """Verifica credenciais e retorna o utilizador autenticado"""
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            logger.info(f"Utilizador {user.email} autenticado.")
            return user
        logger.info(f"Token não gerado. Dados inválidos para o email: {email}")
        return None

    @classmethod
    def create_user(cls, name, email, password, role="user"):
        """Cria um novo utilizador"""
        if not name or not email or not password:
            logger.error("Dados obrigatórios ausentes na criação de utilizador.")
            return {"erro": "Nome, email e senha são obrigatórios!"}, 400

        if not validate_email(email):
            logger.error(f"Email inválido: {email}")
            return {"erro": "Email inválido!"}, 400

        if User.query.filter_by(email=email).first():
            logger.info(f"Tentativa de criar utilizador com email já registado: {email}")
            return {"erro": "Já existe um utilizador com este email!"}, 409

        if role == "admin" and getattr(g, "current_user", None).role != "admin":
            logger.error("Tentativa de criar utilizador admin sem permissão.")
            return {"erro": "Apenas administradores podem criar contas com permissão de admin."}, 403

        if role not in ["admin", "gerente", "estoque", "user"]:
            return {"erro": "Tipo de role inválido!"}, 400

        try:
            hashed_password = generate_password_hash(password)
            new_user = User(name=name, email=email, password=hashed_password, role=role)
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)
            return {"message": "Utilizador criado com sucesso!", "user": new_user.to_dict()}, 201

        except IntegrityError:
            db.session.rollback()
            logger.error("Erro de integridade ao criar utilizador.")
            return {"error": "Erro ao criar utilizador."}, 500

    @classmethod
    def list_users(cls, active=True):
        """Lista utilizadores, com opção de filtrar apenas os ativos"""
        query = User.query
        if active:
            query = query.filter_by(active=True)
        users = query.all()
        return {"users": [u.to_dict() for u in users]}, 200

    @classmethod
    def update_user(cls, user_id, name=None, email=None, password=None, role=None, active=None):
        """Atualiza um utilizador"""
        user = User.query.get(user_id)
        if not user:
            return {"error": "Utilizador não encontrado!"}, 404

        if name:
            user.name = name

        if email:
            if not validate_email(email):
                return {"error": "Email inválido!"}, 400
            user.email = email

        if password:
            user.password = generate_password_hash(password)

        if role is not None:
            if role == "admin" and getattr(g, "current_user", None).role != "admin":
                return {"error": "Apenas administradores podem promover contas para admin."}, 403
            
            if user.role == "admin" and getattr(g, "current_user", None).role != "admin":
                return {"error": "Apenas administradores podem alterar contas de administradores."}, 403
            
            if role not in ["admin", "gerente", "estoque", "user"]:
                return {"error": "Tipo de role inválido!"}, 400
            user.role = role

        if active is not None:
            user.active = active

        try:
            db.session.commit()
            return {"message": "Utilizador atualizado com sucesso!", "utilizador": user.to_dict()}, 200
        
        except Exception as e:

            db.session.rollback()
            logger.error(f"Erro ao atualizar utilizador: {e}")

            return {"erro": "Erro interno ao atualizar utilizador."}, 500

    @classmethod
    def deactivate_user(cls, user_id):
        """Marca um utilizador como inativo"""
        user = User.query.get(user_id)
        if not user:
            return {"erro": "Utilizador não encontrado!"}, 404
        
        user.active = False
        db.session.commit()

        return {"message": f"Utilizador '{user.name}' desativado com sucesso!"}, 200

    @classmethod
    def reactivate_user(cls, user_id):
        """Reativa um utilizador inativo"""
        user = User.query.get(user_id)
        if not user:
            return {"erro": "Utilizador não encontrado!"}, 404
        
        if user.active:
            return {"erro": "O utilizador já está ativo!"}, 400
        
        user.active = True
        db.session.commit()

        return {"message": f"Utilizador '{user.name}' foi reativado com sucesso!", "utilizador": user.to_dict()}, 200
