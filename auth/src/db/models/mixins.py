import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID
from src.db import db


class UUIDMixin:
    __abstract__ = True

    uid = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )


class TimeStampedMixin:
    __abstract__ = True

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
