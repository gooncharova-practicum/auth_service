from http import HTTPStatus

from flask import Blueprint, current_app, url_for
from oauth import oauth
from src.api.v1.models import BaseResponse, GoogleToken, YandexUser
from src.services import oauth_service

app = Blueprint("oauth", __name__, url_prefix="/oauth")


@app.route("/yandex/callback", methods=["GET"])
def yandex_callback() -> tuple[dict[str, str], HTTPStatus]:
    oauth.yandex.authorize_access_token()
    url = "https://login.yandex.ru/info"
    response = oauth.yandex.get(url)
    account_user = YandexUser(**response.json())
    data = oauth_service.login_yandex_user(account_user)
    return BaseResponse(data=data).dict(), HTTPStatus.OK


@app.route("/yandex/login", methods=["GET"])
def yandex_login() -> tuple[dict[str, str], HTTPStatus]:
    oauth = current_app.extensions["authlib.integrations.flask_client"]
    url = url_for("v1.oauth.yandex.callback", _external=True)
    return oauth.yandex.authorize_redirect(url)


@app.route("/google/callback", methods=["GET"])
def google_callback() -> tuple[dict[str, str], HTTPStatus]:
    token = oauth.google.authorize_access_token()

    result = oauth_service.login_google_user(GoogleToken(**token["userinfo"]))

    if result.error_message:
        return (
            BaseResponse(success=False, error=result.error_message).dict(),
            HTTPStatus.UNAUTHORIZED,
        )
    return (BaseResponse(data=result.data).dict(), HTTPStatus.OK)


@app.route("/google/login", methods=["GET"])
def google_login() -> tuple[dict[str, str], HTTPStatus]:
    redirect_uri = url_for("v1.oauth.google.callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
