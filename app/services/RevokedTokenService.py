from app.extensions import db
from app.models.Revoked_Token import RevokedToken
from app.utils.logger_util import get_logger

logger = get_logger(__name__)

class TokenService:
    """Gerencia a blacklist de tokens JWT"""

    @classmethod
    def add_to_blacklist(cls, token_jti):
        """Adiciona um token revogado ao banco de dados"""
        revoked = RevokedToken(token_jti=token_jti)
        db.session.add(revoked)
        db.session.commit()
        logger.info(f"Token revogado cadastrado: {token_jti}")

    @classmethod
    def in_blacklist(cls, token_jti: str) -> bool:
        """Verifica se um token está na blacklist"""
        return RevokedToken.query.filter_by(token_jti=token_jti).first() is not None
