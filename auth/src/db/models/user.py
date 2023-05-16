from sqlalchemy import UUID
from src.db import db

from .mixins import TimeStampedMixin, UUIDMixin


class User(db.Model, UUIDMixin, TimeStampedMixin):
    __tablename__ = "user"

    login = db.Column(db.String(length=100), unique=True, nullable=False)
    first_name = db.Column(db.String(length=150), nullable=False)
    last_name = db.Column(db.String(length=150))
    roles = db.relationship("Role", secondary="user_role", back_populates="users")
    password = db.Column(db.String(length=150), nullable=False)
    email = db.Column(db.String(length=64), nullable=False, unique=True)
    login_history = db.relationship("LoginHistory", backref="user")
    is_active = db.Column(db.Boolean)
    is_deleted = db.Column(db.Boolean, default=False)
    jwts = db.relationship("JWTStore", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User: {self.login}>"


class SocialAccount(db.Model, UUIDMixin):
    __tablename__ = "social_account"

    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(User.uid, ondelete="CASCADE"),
        nullable=False,
    )
    user = db.relationship(User, backref=db.backref("social_account", lazy=True))
    social_id = db.Column(db.String(128), nullable=False)
    social_name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<SocialAccount {self.social_name}:{self.user_id}>"


class Role(db.Model, UUIDMixin):
    __tablename__ = "roles"

    name = db.Column(db.String(length=32), unique=True, nullable=False)
    description = db.Column(db.String(length=200))
    users = db.relationship("User", secondary="user_role", back_populates="roles")

    def __repr__(self):
        return f"{self.__class__.name} {self.name}"


class UserRole(db.Model, UUIDMixin):
    __tablename__ = "user_role"

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(User.uid, ondelete="CASCADE"))
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Role.uid, ondelete="CASCADE"))
