import datetime
from enum import Enum

from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import INET
from src.db import db
from src.db.models.user import User
from user_agents import parse

from .mixins import UUIDMixin


class DeviceType(Enum):
    smart = "smart"
    mobile = "mobile"
    tablet = "tablet"
    web = "web"


def create_partition(target, connection, **kw) -> None:
    """creating partition by user_sign_in"""
    connection.execute(
        f"""CREATE TABLE IF NOT EXISTS "smart_login_history" PARTITION OF
                                        "login_history" FOR VALUES IN ('{DeviceType.smart}')"""
    )
    connection.execute(
        f"""CREATE TABLE IF NOT EXISTS "mobile_login_history" PARTITION OF
                                        "login_history" FOR VALUES IN ('{DeviceType.mobile}')"""
    )
    connection.execute(
        f"""CREATE TABLE IF NOT EXISTS "web_login_history" PARTITION OF
                                        "login_history" FOR VALUES IN ('{DeviceType.web}')"""
    )
    connection.execute(
        f"""CREATE TABLE IF NOT EXISTS "tablet_login_history" PARTITION OF
                                        "login_history" FOR VALUES IN ('{DeviceType.tablet}')"""
    )


class LoginHistory(db.Model, UUIDMixin):
    __tablename__ = "login_history"
    __table_args__ = {
        "postgresql_partition_by": "LIST (device_type)",
        "listeners": [("after_create", create_partition)],
    }

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(User.uid, ondelete="CASCADE"))
    user_agent = db.Column(db.String(length=200))
    ip_address = db.Column(INET, nullable=False)
    device_type = db.Column(db.String(length=20))
    auth_datetime = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

    def __repr__(self):
        return f"Last login {self.ip_address}: {self.auth_datetime}"

    @property
    def user_device_type(self):
        return self.device_type

    @user_device_type.setter
    def device_type(self, agent_string):
        user_agent = parse(agent_string)
        if user_agent.is_mobile:
            self.device_type = DeviceType.mobile
        elif user_agent.is_pc:
            self.device_type = DeviceType.web
        elif user_agent.is_tablet:
            self.device_type = DeviceType.tablet
        else:
            self.device_type = DeviceType.smart
