from sqlalchemy.dialects.postgresql import UUID
from src.db import db

from .mixins import UUIDMixin
from .user import User


class JWTStore(db.Model, UUIDMixin):
    __tablename__ = "jwt_store"

    jwt_id = db.Column(UUID(as_uuid=True), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.UUID, db.ForeignKey(User.uid, ondelete="CASCADE"), nullable=False)
    type = db.Column(db.String(length=15), nullable=False)
