import uuid
from http import HTTPStatus

import allure
import pytest
from mylib import Assert

ROLES = "/roles"


@allure.title("Roles info")
@pytest.mark.asyncio
async def test_roles_info(make_get_request, expected_json_response):
    uid = str(uuid.uuid4())
    response = await make_get_request(f"{ROLES}/{uid}")
    Assert(response).status_code(HTTPStatus.NOT_FOUND).body_is(expected_json_response)


@allure.title("Roles list")
@pytest.mark.asyncio
async def test_roles_list(make_get_request, expected_json_response):
    response = await make_get_request(f"{ROLES}/")
    Assert(response).status_code(HTTPStatus.OK).body_is(expected_json_response)


@allure.title("Create role")
@pytest.mark.asyncio
async def test_create_role(make_post_request, expected_json_response):
    body = {"name": "test_role", "description": "let's test roles created"}
    response = await make_post_request(f"{ROLES}/create", body=body)
    Assert(response).status_code(HTTPStatus.CREATED).body_is(expected_json_response)


@allure.title("Create role with long name")
@pytest.mark.asyncio
async def test_create_role_with_long_name(make_post_request, expected_json_response):
    body = {
        "name": "Newrole_newrole_newrole_newrole_newrole",
        "description": "we can't create with long name",
    }
    response = await make_post_request(f"{ROLES}/create", body=body)
    Assert(response).status_code(HTTPStatus.BAD_REQUEST).body_is(expected_json_response)
