from gevent import monkey

monkey.patch_all()  # noqa

from datetime import timedelta

from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager
from oauth import oauth
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from src.api import v1
from src.cli_commands import superuser_creation_command
from src.core import (
    flask_config,
    jaeger_config,
    jwt_config,
    oauth_google,
    oauth_yandex,
    redis_config,
    swagger_config,
)
from src.db import init_db
from src.db.redis import jwt, jwt_redis_blocklist
from src.services.limiter import limiter
from src.utils import after_request_log, before_request_jaeger, before_request_log, configure_tracer
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app():
    app = Flask(__name__)

    # for jaeger
    if jaeger_config.JAEGER_ENABLED:
        app.before_request(before_request_jaeger)
        configure_tracer()

    app.config["JSON_AS_ASCII"] = False
    app.config["SECRET_KEY"] = flask_config.SECRET_KEY

    limiter.init_app(app)
    FlaskInstrumentor().instrument_app(app)

    JWTManager(app)

    # swagger
    Swagger(app, config=swagger_config.CONFIG, template=swagger_config.TEMPLATE)

    # redis & jwt
    app.config["REDIS_URL"] = redis_config.REDIS_DSN
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=jwt_config.ACCESS_EXP)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=jwt_config.REFRESH_EXP)

    jwt_redis_blocklist.init_app(app, decode_responses=True)
    jwt.init_app(app)

    # request logging
    app.before_request(before_request_log)
    app.after_request(after_request_log)

    # routing
    app.register_blueprint(v1.bp)

    # DB
    init_db(app)

    # create_superuser
    app.cli.add_command(superuser_creation_command(app))

    # oauth
    app.config.update(oauth_yandex.dict())
    app.config.update(oauth_google.dict())

    oauth.init_app(app)

    oauth.register(name="yandex")
    oauth.register(
        name="google",
        server_metadata_url=oauth_google.CONF_URL,
        client_kwargs={"scope": oauth_google.scope},
    )

    # App is behind one proxy (nginx) that sets the -For and host headers.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    return app


if __name__ == "__main__":
    # for debug, local running
    app = create_app()
    app.run(
        host=flask_config.HOST,
        port=flask_config.FLASK_PORT,
        debug=flask_config.DEBUG,
    )
