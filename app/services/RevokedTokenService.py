from app.database import Database
from app.models.Revoked_Token import RevokedToken
from app.util.logger_util import get_logger

logger= get_logger(__name__)

class TokenService:
    """Gerencia a blacklist de tokens JWT"""

    @staticmethod
    def add_token_to_blacklist(token_jti):
        """Adiciona um token revogado ao banco de dados"""
        token_revoked= RevokedToken(token_jti=token_jti)
        logger.info(f"Token revogado: {token_revoked}")

        session = Database.get_session()
        session.add(token_revoked)
        session.commit()

    @staticmethod
    def token_on_blacklist(token_jti):
        """Verifica se um token está na blacklist"""
        session = Database.get_session()
        return session.query(RevokedToken).filter_by(token_jti=token_jti).first() is not None
