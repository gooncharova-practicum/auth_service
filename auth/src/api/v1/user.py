from http import HTTPStatus

from flasgger import swag_from
from flask import Blueprint
from flask_jwt_extended import jwt_required
from pydantic import UUID4
from src.api.v1.models import BaseResponse, GetUserModel, LoginHistory, UpdateUser
from src.api.v1.utils import get_body
from src.core import swagger_config
from src.services.limiter import limiter
from src.services.user import UserCrud

user_crud = UserCrud()

app = Blueprint("user", __name__, url_prefix="/user")


@app.route("/<user_id>", methods=["GET"])
@limiter.limit("4/minute")
@swag_from(f"{swagger_config.SPECS_DIR}/get-user.yaml")
def get_user_info(user_id: UUID4):
    base_result = user_crud.get_user_info(user_id)
    if base_result.error_message:
        return (
            BaseResponse(success=False, error=base_result.error_message).dict()
        ), HTTPStatus.NOT_FOUND
    result = base_result.data
    data = GetUserModel(
        login=result.login,
        first_name=result.first_name,
        last_name=result.last_name,
        email=result.email,
        is_active=result.is_active,
        is_deleted=result.is_deleted,
    )
    return BaseResponse(success=True, data=data).dict(), HTTPStatus.OK


@app.route("/<user_id>", methods=["DELETE"])
@jwt_required()
@swag_from(f"{swagger_config.SPECS_DIR}/delete-user.yaml")
def delete_user(user_id: UUID4):
    result = user_crud.delete_user(user_id)
    if result.error_message:
        return (
            BaseResponse(success=False, error=result.error_message).dict()
        ), HTTPStatus.NOT_FOUND
    return BaseResponse(success=True, data="Success").dict(), HTTPStatus.OK


@app.route("/<user_id>", methods=["PATCH"])
@jwt_required(refresh=True)
@swag_from(f"{swagger_config.SPECS_DIR}/update-user.yaml")
def edit_user(user_id: UUID4):
    body: UpdateUser = get_body(UpdateUser)
    base_result = user_crud.update_user_info(user_id, body)
    if base_result.error_message:
        return (
            BaseResponse(success=False, error=base_result.error_message).dict()
        ), HTTPStatus.NOT_FOUND
    result = base_result.data
    data = UpdateUser(
        first_name=result.first_name,
        last_name=result.last_name,
        email=result.email,
        is_active=result.is_active,
        password=result.password,
    )
    return BaseResponse(success=True, data=data).dict(), HTTPStatus.OK


@app.route("/login/history/<user_id>", methods=["GET"])
@jwt_required(refresh=True)
@swag_from(f"{swagger_config.SPECS_DIR}/get_login_history.yaml")
def get_login_history(user_id: UUID4):
    base_result = user_crud.get_login_history(user_id)
    if base_result.error_message:
        return (
            BaseResponse(success=False, error=base_result.error_message).dict()
        ), HTTPStatus.NOT_FOUND
    result = base_result.data
    body = [
        LoginHistory(
            user_id=user_id,
            user_agent=i.user_agent,
            ip_address=i.ip_address,
            device_type=i.device_type,
        )
        for i in result
    ]
    return BaseResponse(success=True, data=body).dict(), HTTPStatus.OK
