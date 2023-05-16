from flask import Blueprint
from src.api.v1 import auth, oauth, roles, user

bp = Blueprint("v1", __name__, url_prefix="/api/v1")

bp.register_blueprint(auth.app)
bp.register_blueprint(oauth.app)
bp.register_blueprint(roles.app)
bp.register_blueprint(user.app)
