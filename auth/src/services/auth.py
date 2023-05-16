from dataclasses import dataclass
from datetime import datetime

from flask import current_app, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jti,
)
from src.api.v1.models import TokenData
from src.core import logger, user_roles
from src.db.models import JWTStore, LoginHistory, Role, User
from src.db.redis import check_if_token_is_revoked, jwt_redis_blocklist
from src.services.db_manager import Cursor
from src.services.models import ServiceResult
from user_agents import parse

cur = Cursor()


def signup(
    login: str,
    first_name: str,
    email: str,
    password: str,
) -> ServiceResult:
    first_email = cur.get_first_match(User, User.email, email)
    if first_email:
        error_message = "Login or email already exists"
        logger.info("User already exists")
        return ServiceResult(success=False, error_message=error_message)

    user = User(
        login=login,
        first_name=first_name,
        email=email,
        password=password,
    )

    cur.add(user)
    user_role = cur.get_first_match(Role, Role.name, user_roles.user)
    user.roles.append(user_role)
    cur.add(user)

    user = cur.get_first_match(User, User.email, email)
    logger.info("User created")

    return ServiceResult(success=True, data=user)


def login(
    login: str | None,
    password: str | None,
    user_agent: str | None,
) -> ServiceResult:
    user = cur.get_first_match(User, User.login, login)

    if user and user.password == password:
        user_device_type = _get_device_type(user_agent)

        cur.add(
            LoginHistory(
                user_id=user.uid,
                ip_address=request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                user_agent=user_agent,
                device_type=user_device_type,
                auth_datetime=datetime.now(),
            )
        )
        tokens = _create_tokens(user)
        return ServiceResult(success=True, data=tokens)

    return ServiceResult(success=False, error_message="Wrong login or password")


def refresh_token(
    user: User,
    old_refresh_token_jti: str,
) -> ServiceResult:
    old_refresh_token = JWTStore.query.filter_by(
        user_id=user.id, jwt_id=old_refresh_token_jti
    ).one_or_none()

    if old_refresh_token:
        cur.delete(JWTStore, JWTStore.jwt_id, old_refresh_token)
    _invalidate_jwt(old_refresh_token_jti, "refresh")

    jwt_tokens = _create_tokens(user)
    return ServiceResult(success=True, data=jwt_tokens)


def logout(
    user: User,
    tokens_to_logout: list,
) -> ServiceResult:
    for token in JWTStore.query.filter_by(user_id=user.uid).all():
        if token.jwt_id in tokens_to_logout:
            _invalidate_jwt(token.jwt_id, token.type)
            cur.delete(JWTStore, JWTStore.token, token)

    for token in JWTStore.query.filter_by(user_id=user.id).all():
        if token.jwt_id in tokens_to_logout:
            _invalidate_jwt(token.jwt_id, token.type)
            cur.delete(JWTStore, JWTStore.token, token)

    return ServiceResult(success=True)


def _invalidate_jwt(jti, token_type):
    if token_type == "access":
        expiration_date = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    elif token_type == "refresh":
        expiration_date = current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]
    jwt_redis_blocklist.set(jti, "", ex=expiration_date)


def _create_tokens(user) -> tuple[str, str]:
    access_token = create_access_token(identity=user)
    access_token_exp_date = datetime.now() + current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]

    refresh_token = create_refresh_token(identity=user)
    refresh_token_exp_date = datetime.now() + current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]

    cur.add(
        JWTStore(
            jwt_id=get_jti(access_token),
            expiration_date=access_token_exp_date,
            user_id=user.uid,
            type="access",
        )
    )

    cur.add(
        JWTStore(
            jwt_id=get_jti(refresh_token),
            expiration_date=refresh_token_exp_date,
            user_id=user.uid,
            type="refresh",
        )
    )

    return TokenData(
        access_token=access_token,
        access_token_expiration_date=access_token_exp_date,
        refresh_token=refresh_token,
        refresh_token_expiration_date=refresh_token_exp_date,
    )


def _get_device_type(user_agent_string: str):
    @dataclass
    class DeviceType:
        PC = "web"
        MOBILE = "mobile"
        TABLET = "tablet"

    device_types = DeviceType
    user_agent = parse(user_agent_string)

    if user_agent.is_mobile:
        return device_types.MOBILE
    elif user_agent.is_tablet:
        return device_types.TABLET
    return device_types.PC


def token_validator(jwt_payload):
    return check_if_token_is_revoked(jwt_payload)
