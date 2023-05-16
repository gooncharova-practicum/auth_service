from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = "migrations"


load_dotenv()


class EnvBaseSettings(BaseSettings):
    class Config:
        env_file = "./.env"


class FlaskConfig(EnvBaseSettings):
    DEBUG: bool = Field(default=False == "True")
    HOST: str
    PORT: int
    FLASK_PORT: int
    SECRET_KEY: str


class BaseConfig(EnvBaseSettings):
    COMMON_SERVICE_NAME: str
    REQUEST_LIMIT: str


class JwtConfig(EnvBaseSettings):
    ACCESS_EXP: int
    REFRESH_EXP: int


class RedisConfig(EnvBaseSettings):
    REDIS_DSN: str
    MAX_WAITING_TIME: int
    KEY_TTL: int


class PGConfig(EnvBaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_DSN: str


class UserRoles(EnvBaseSettings):
    admin: str = Field(default="admin")
    user: str = Field(default="user")
    sub: str = Field(default="sub")
    superuser: str = Field(default="superuser")


class JaegerConfig(EnvBaseSettings):
    JAEGER_HOSTNAME: str
    JAEGER_SERVICE_PORT: int
    JAEGER_EXTERNAL_PORT: int
    JAEGER_ENABLED: bool


class SwaggerConfig(BaseSettings):
    TEMPLATE = {
        "swagger": "2.0",
        "info": {
            "title": "Authorization service API",
            "description": "API for authorization service",
        },
        "basePath": "/api/v1",
        "schemes": ["http", "https"],
        "securityDefinitions": {
            "APIKeyHeader": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "\
                    Type in the *'Value'* input box below: \
                        **'Bearer JWT;'**, where JWT is the token",
            }
        },
    }

    CONFIG = {
        "headers": [],
        "specs": [
            {
                "endpoint": "api/spec",
                "route": "/api/spec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs/",
    }

    SPECS_DIR = str(BASE_DIR / "static" / "specs")


class OAuthYandexSettings(EnvBaseSettings):
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_ACCESS_TOKEN_URL: str
    YANDEX_AUTHORIZE_URL: str


class OAuthGoogleSettings(EnvBaseSettings):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    CONF_URL: str = "https://accounts.google.com/.well-known/openid-configuration"
    scope: str = "openid email profile"


flask_config = FlaskConfig()
jwt_config = JwtConfig()
redis_config = RedisConfig()
pg_config = PGConfig()
user_roles = UserRoles()
swagger_config = SwaggerConfig()
jaeger_config = JaegerConfig()
base_config = BaseConfig()
oauth_yandex = OAuthYandexSettings()
oauth_google = OAuthGoogleSettings()
