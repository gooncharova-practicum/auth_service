from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from src.db.models import User

jwt_redis_blocklist = FlaskRedis()
jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.uid


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
