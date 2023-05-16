from typing import Callable

import click
from flask import Flask
from src.core import logger
from src.core.config import UserRoles
from src.db.models import Role, User
from src.services.db_manager import Cursor


def superuser_creation_command(app: Flask) -> Callable:
    @app.cli.command("create_superuser")
    @click.argument("login")
    @click.argument("first_name")
    @click.argument("email")
    @click.argument("password")
    def create_superuser(login: str, first_name: str, email: str, password: str) -> None:
        cur = Cursor()
        first_user = cur.get_first_match(User, User.login, login)

        if not first_user:
            superuser_role = cur.get_first_match(Role, Role.name, UserRoles.superuser)
            superuser = User(
                login=login,
                first_name=first_name,
                email=email,
                password=password,
            )
            cur.add(superuser)
            superuser.roles.append(superuser_role)

            logger.info("Superuser created succesfully")

        logger.info(f"User with login {login} already exist")

    return create_superuser
