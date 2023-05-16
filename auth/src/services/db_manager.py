from uuid import UUID

from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from src.api.v1.models import GetUserModel, UpdateUser
from src.core import pg_config
from src.db import db


class DBSession:
    def __init__(self, pg_dsn: str, autocommit: bool = False, expire_on_commit: bool = False):
        self.engine = create_engine(pg_dsn, echo=False)
        self.session_local = sessionmaker(
            autocommit=autocommit,
            autoflush=False,
            bind=self.engine,
            expire_on_commit=expire_on_commit,
        )

    def session(self):
        return self.session_local()


_db_session = DBSession(pg_config.DB_DSN).session()


class Cursor:
    def __init__(self, session: sessionmaker = _db_session):
        self.session = session

    def get_first_match(self, model: db.Model, column: db.Column, value: str) -> str | None:
        return self.session.query(model).filter(column == value).first()

    def get_all_items(self, model: db.Model):
        return self.session.query(model).all()

    def add(self, model: db.Model) -> None:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

    def update(self, model: db.Model, column: db.Column, filter_value: str, values: dict) -> None:
        self.session.query(model).filter(column == filter_value).update(values)
        self.session.commit()
        self.session.refresh(model)

    def delete(self, model: db.Model, column: db.Column, value: str) -> str | None:
        self.session.query(model).filter(column == value).delete()

    def get_user(self, model: db.Model, column: db.Column, value: str) -> GetUserModel | None:
        result = (
            self.session.query(model)
            .filter(column == value, model.is_deleted == False)  # NOQA: E712
            .first()
        )
        return result

    def delete_user(
        self, model: db.Model, column: db.Column, value: str, user_data: GetUserModel
    ) -> str | None:
        user_data.is_delete = True
        self.session.execute(update(model).where(column == value).values(is_deleted=True))
        self.session.commit()
        self.session.refresh(user_data)
        return "OK"

    def get_all_items_by_id(self, model: db.Model, column: db.Column, user_id: UUID):
        return self.session.query(model).filter(column == user_id).all()

    def update_user(
        self,
        model: db.Model,
        column: db.Column,
        value: str,
        body: UpdateUser,
        user_data: GetUserModel,
    ):
        result = self.get_user(model, column, value)
        self.session.execute(
            update(model)
            .where(column == value)
            .values(
                first_name=body.first_name,
                last_name=body.last_name,
                email=body.email,
                is_active=body.is_active,
                password=body.password,
            )
        )
        self.session.commit()
        self.session.refresh(result)
        return result
