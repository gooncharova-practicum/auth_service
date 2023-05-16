from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.core import MIGRATIONS_DIR, pg_config

db = SQLAlchemy()


def init_db(app: Flask):
    """Initialization of pg database"""

    app.config["SQLALCHEMY_DATABASE_URI"] = pg_config.DB_DSN
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.app_context().push()
    db.init_app(app)

    return db
