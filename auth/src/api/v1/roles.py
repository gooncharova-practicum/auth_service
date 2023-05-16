from http import HTTPStatus

from flasgger import swag_from
from flask import Blueprint
from flask_jwt_extended import jwt_required
from pydantic import UUID4
from src.api.v1.models import BaseResponse, NewRole, Role, UpdatedRole
from src.api.v1.utils import get_body, superuser_only
from src.core import errors, swagger_config
from src.services import roles

app = Blueprint("roles", __name__, url_prefix="/roles")


@app.route("/", methods=["GET"])
@jwt_required()
@superuser_only()
@swag_from(f"{swagger_config.SPECS_DIR}/get_roles_list.yaml")
def get_roles_list():
    all_roles = roles.get_roles_list()
    data = [
        Role(uuid=role.uid, name=role.name, description=role.description) for role in all_roles.data
    ]
    return BaseResponse(success=True, data=data).dict(), HTTPStatus.OK


@app.route("/<role_id>", methods=["GET"])
@jwt_required()
@superuser_only()
@swag_from(f"{swagger_config.SPECS_DIR}/get_role_info.yaml")
def get_role_info(role_id: UUID4):
    result = roles.get_roles_info(role_id)
    if result.error_message:
        return (
            BaseResponse(success=False, error=str(result.error_message)).dict(),
            HTTPStatus.NOT_FOUND,
        )
    data = Role(result.data.uid, result.data.name, result.data.description)
    return BaseResponse(success=True, data=data).dict(), HTTPStatus.OK


@app.route("/create", methods=["POST"])
@jwt_required()
@superuser_only()
@swag_from(f"{swagger_config.SPECS_DIR}/create_role.yaml")
def create_role():
    """
    :param str name
    :param str description
    """
    try:
        body: NewRole = get_body(NewRole)
        result = roles.create_role(body.name, body.description)

        if result.error_message:
            return (
                BaseResponse(success=False, error=str(result.error_message)).dict(),
                HTTPStatus.CONFLICT,
            )
        data = Role(uid=result.data.uid, name=result.data.name, descripton=result.data.description)
        return BaseResponse(success=True, data=data).dict(), HTTPStatus.CREATED

    except errors.LenOfValueError as e:
        return BaseResponse(success=False, error=str(e)).dict(), HTTPStatus.BAD_REQUEST


@app.route("/<role_id>", methods=["PATCH"])
@jwt_required()
@superuser_only()
@swag_from(f"{swagger_config.SPECS_DIR}/update_role.yaml")
def update_role(role_id: UUID4):
    """
    :param str name
    :param str description
    """
    try:
        body: UpdatedRole = get_body(UpdatedRole)
        result = roles.update_role(role_id, body.name, body.description)
        if result.error_message:
            return (
                BaseResponse(success=False, error=str(result.error_message)).dict(),
                HTTPStatus.BAD_REQUEST,
            )
        data = Role(uid=result.data.uid, name=result.data.name, descripton=result.data.description)
        return BaseResponse(success=True, data=data).dict(), HTTPStatus.OK
    except errors.LenOfValueError as e:
        return BaseResponse(success=False, error=str(e)).dict(), HTTPStatus.BAD_REQUEST


@app.route("/<role_id>", methods=["DELETE"])
@jwt_required()
@superuser_only()
@swag_from(f"{swagger_config.SPECS_DIR}/delete_role.yaml")
def delete_role(role_id: UUID4):
    result = roles.delete_role(role_id)
    if result.error_message:
        return (
            BaseResponse(success=False, error=str(result.error_message)).dict(),
            HTTPStatus.NOT_FOUND,
        )

    return BaseResponse(success=True, data=None).dict(), HTTPStatus.NO_CONTENT
