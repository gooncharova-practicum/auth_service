import secrets
import string
from dataclasses import dataclass
from typing import Callable

from src.api.v1.models import GoogleToken, YandexUser
from src.db import db
from src.db.models import SocialAccount, User
from src.services import auth, db_manager
from src.services.models import ServiceResult


@dataclass
class SocialName:
    YANDEX = "yandex"
    GOOGLE = "google"


cursor = db_manager.Cursor()


def login_yandex_user(account_user: YandexUser) -> Callable:
    return _social_login_or_register(
        email=account_user.email,
        social_id=account_user.id,
        social_name=SocialName.YANDEX,
        social_login=account_user.login,
    )


def login_google_user(token: GoogleToken) -> Callable:
    if not token.email_verified:
        return ServiceResult(success=False, error_message="Need to verify email")

    return _social_login_or_register(
        email=token.email,
        social_id=token.sub,
        social_name=SocialName.GOOGLE,
    )


def _create_random_alphanumeric_string():
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(30))


def _social_login_or_register(
    email: str,
    social_id: str,
    social_name: SocialName,
    social_login: str | None = None,
):
    social_account = cursor.get_first_match(SocialAccount, SocialAccount.social_id, social_id)

    if not social_account:
        login_attempt = auth.login(login=None, email=email, password=None, is_social_auth=True)

        if login_attempt.success:
            user = User.query.filter_by(email=email).one_or_none()
        else:
            registration_attempt = auth.signup(
                login=social_login or _create_random_alphanumeric_string(),
                email=email,
                password=_create_random_alphanumeric_string(),
            )

            if registration_attempt.success:
                user = registration_attempt.data
            else:
                return registration_attempt

        social_account = SocialAccount(
            social_id=social_id,
            social_name=social_name,
            user_id=user.id,
        )
        db.session.add(social_account)
        db.session.commit()

    return auth.login(social_account.user.login, None, is_social_auth=True)
