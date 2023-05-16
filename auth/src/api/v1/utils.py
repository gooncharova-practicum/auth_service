from functools import wraps
from typing import Any

from flask import abort, request
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from pydantic import BaseModel, ValidationError
from src.core import logger
from src.core.config import UserRoles


def get_body(request_model: type[BaseModel]):
    try:
        body = request_model.parse_obj(request.get_json())
    except ValidationError as err:
        logger.error(f"{err.__class__.__name__}: {err}")
        error_message = err.errors()
        abort(400, description=error_message)
    else:
        return body


def superuser_only():
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs) -> Any | dict[str, str]:
            verify_jwt_in_request()
            jwt_fields = get_jwt()
            if jwt_fields["role"] == UserRoles.superuser:
                return func(*args, **kwargs)
            return {"response": "action is available only for superusers"}

        return decorator

    return wrapper
