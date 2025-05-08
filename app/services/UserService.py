from app.database import Database
from app.models.User import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.logger_util import get_logger
from app.util.validate_email_phone import validate_email
from flask import g

class UserService:
    """Gerencia autenticação e operações com usuários"""

    logger = get_logger(__name__)

    @classmethod
    def auth_user(cls, email, password):
        """Verifica credenciais e retorna o utilizador autenticado"""
        session = Database.get_session()
        try:
            user = session.query(User).filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                cls.logger.info(f"Utilizador {user.email} autenticado.")
                return user

            cls.logger.info(f"Token não gerado. Dados inválidos para o email: {email}")
            return None
        finally:
            session.close()

    @classmethod
    def create_user(cls, name, email, password, role="user"):
        """Cria um novo utilizador"""
        session = Database.get_session()
        try:
            if not name or not email or not password:
                cls.logger.error("Dados obrigatórios ausentes na criação de utilizador.")
                return {"erro": "Nome, email e senha são obrigatórios!"}, 400

            if not validate_email(email):
                cls.logger.error(f"Email inválido: {email}")
                return {"erro": "Email inválido!"}, 400

            if session.query(User).filter_by(email=email).first():
                cls.logger.info(f"Tentativa de criar utilizador com email já registado: {email}")
                return {"erro": "Já existe um utilizador com este email!"}, 409

            if role == "admin" and g.current_user.role != "admin":
                cls.logger.error("Tentativa de criar utilizador admin sem permissão.")
                return {"erro": "Apenas administradores podem criar contas com permissão de admin."}, 403

            if role not in ["admin", "gerente", "estoque", "user"]:
                return {"erro": "Tipo de role inválido!"}, 400

            hashed_password = generate_password_hash(password)
            new_user = User(name=name, email=email, password=hashed_password, role=role)

            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            return {
                "mensagem": "Utilizador criado com sucesso!",
                "utilizador": new_user.to_dict()
            }, 201

        except IntegrityError:
            session.rollback()
            cls.logger.error("Erro de integridade ao criar utilizador.")
            return {"erro": "Erro ao criar utilizador."}, 500
        finally:
            session.close()

    @classmethod
    def list_users(cls, active=True):
        """Lista utilizadores, com opção de filtrar apenas os ativos"""
        session = Database.get_session()
        try:
            query = session.query(User)
            if active:
                query = query.filter_by(active=True)
            users = query.all()
            return {"utilizadores": [user.to_dict() for user in users]}, 200
        finally:
            session.close()

    @classmethod
    def update_user(cls, user_id, name=None, email=None, password=None, role=None, active=None):
        """Atualiza um utilizador"""
        session = Database.get_session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return {"erro": "Utilizador não encontrado!"}, 404

            if name:
                user.name = name

            if email:
                if not validate_email(email):
                    return {"erro": "Email inválido!"}, 400
                user.email = email

            if password:
                user.password = generate_password_hash(password)

            if role is not None:
                if role == "admin" and g.current_user.role != "admin":
                    return {"erro": "Apenas administradores podem promover contas para admin."}, 403

                if user.role == "admin" and g.current_user.role != "admin":
                    return {"erro": "Apenas administradores podem alterar contas de administradores."}, 403

                if role not in ["admin", "gerente", "estoque", "user"]:
                    return {"erro": "Tipo de role inválido!"}, 400

                user.role = role

            if active is not None:
                user.active = active

            session.commit()
            return {
                "mensagem": "Utilizador atualizado com sucesso!",
                "utilizador": user.to_dict()
            }, 200

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao atualizar utilizador: {e}")
            return {"erro": "Erro interno ao atualizar utilizador."}, 500
        finally:
            session.close()

    @classmethod
    def deactivate_user(cls, user_id):
        """Marca um utilizador como inativo"""
        session = Database.get_session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return {"erro": "Utilizador não encontrado!"}, 404

            user.active = False
            session.commit()
            return {"mensagem": f"Utilizador '{user.name}' desativado com sucesso!"}, 200
        finally:
            session.close()

    @classmethod
    def reactivate_user(cls, user_id):
        """Reativa um utilizador inativo"""
        session = Database.get_session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return {"erro": "Utilizador não encontrado!"}, 404

            if user.active:
                return {"erro": "O utilizador já está ativo!"}, 400

            user.active = True
            session.commit()
            return {
                "mensagem": f"Utilizador '{user.name}' foi reativado com sucesso!",
                "utilizador": user.to_dict()
            }, 200
        finally:
            session.close()
