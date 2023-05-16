from http import HTTPStatus

import allure
import pytest
from mylib import Assert

AUTH = "/auth"


@allure.title("Sign up")
@pytest.mark.asyncio
async def test_signup(make_post_request, expected_json_response):
    body = {"login": "li", "first_name": "li", "email": "li@mail.ru", "password": "li"}
    response = await make_post_request(f"{AUTH}/signup", body=body)
    Assert(response).status_code(HTTPStatus.NOT_FOUND).body_is(expected_json_response)


@allure.title("Logout")
@pytest.mark.asyncio
async def test_logout(make_post_request, expected_json_response):
    body = {
        "refresh_token": "fake_token",
    }
    response = await make_post_request(f"{AUTH}/logout", body=body)
    Assert(response).status_code(HTTPStatus.NOT_FOUND).body_is(expected_json_response)
