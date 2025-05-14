from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.models.BaseModel import BaseModel

class RevokedToken(BaseModel):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True)
    token_jti = Column(String, nullable=False, unique=True)  # ID único do token
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))