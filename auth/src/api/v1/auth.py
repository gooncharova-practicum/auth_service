from http import HTTPStatus

from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt_extended import current_user, get_jti, get_jwt, jwt_required
from src.api.v1.models import (
    BaseResponse,
    JwtTokenModel,
    LoginUserRequest,
    LogoutUser,
    RegUserRequest,
    UserData,
)
from src.api.v1.utils import get_body
from src.core import errors, swagger_config
from src.services import auth

app = Blueprint("auth", __name__, url_prefix="/auth")


@app.route("/signup", methods=["POST"])
@swag_from(f"{swagger_config.SPECS_DIR}/signup.yaml")
def signup() -> tuple[dict[str, str], HTTPStatus]:
    """
    :param str login
    :param str first_name
    :param str email
    :param str password
    """
    try:
        body: RegUserRequest = get_body(RegUserRequest)

        result = auth.signup(
            login=body.login,
            first_name=body.first_name,
            email=body.email,
            password=body.password,
        )

        if result.error_message:
            return (
                BaseResponse(success=False, error=result.error_message).dict()
            ), HTTPStatus.BAD_REQUEST

        data = UserData(uid=result.data.uid, login=result.data.login, email=result.data.email)
        return BaseResponse(success=True, data=data).dict(), HTTPStatus.OK

    except errors.LenOfValueError as e:
        return (BaseResponse(success=False, error=str(e)).dict()), HTTPStatus.BAD_REQUEST


@app.route("/login", methods=["POST"])
@swag_from(f"{swagger_config.SPECS_DIR}/login.yaml")
def login():
    """
    :param str login
    :param str password
    """
    useragent = request.headers.get("User-Agent")
    body: LoginUserRequest = get_body(LoginUserRequest)

    result = auth.login(login=body.login, password=body.password, user_agent=useragent)

    if result.error_message:
        return (
            BaseResponse(success=False, error="Wrong username or password").dict(),
            HTTPStatus.UNAUTHORIZED,
        )
    return (
        BaseResponse(data=result.data).dict(),
        HTTPStatus.OK,
    )


@app.route("/validate", methods=["POST"])
def validator():
    body: JwtTokenModel = get_body(JwtTokenModel)
    result = auth.token_validator(body.token)

    return (
        BaseResponse(data=result).dict(),
        HTTPStatus.OK,
    )


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@swag_from(f"{swagger_config.SPECS_DIR}/refresh.yaml")
def refresh_token():
    """
    :param str refresh_token
    """
    old_refresh_token_jti = get_jwt()["jti"]
    result = auth.refresh_token(current_user, old_refresh_token_jti)

    return (
        BaseResponse(success=result.success, data=result.data).dict(),
        HTTPStatus.OK,
    )


@app.route("/logout", methods=["POST"])
@jwt_required()
@swag_from(f"{swagger_config.SPECS_DIR}/logout.yaml")
def logout():
    """
    :param str refresh_token
    """
    body: LogoutUser = get_body(LogoutUser)

    current_tokens = [get_jwt()["jti"], get_jti(body.refresh_token)]
    result = auth.logout(current_user, current_tokens)

    return BaseResponse(success=result.success).dict(), HTTPStatus.OK
