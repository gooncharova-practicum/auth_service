import os
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import BaseSettings

from .logger import LOGGING

load_dotenv()

logging_config.dictConfig(LOGGING)


class ProjectModel(BaseSettings):
    PROJECT_NAME: str = "movies"
    BACKEND_PORT: int

    class Config:
        env_file = "./.env"


class RedisModel(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = "./.env"


class ElasticModel(BaseSettings):
    ELASTIC_HOST: str
    ELASTIC_PORT: int

    class Config:
        env_file = "./.env"


class AuthModel(BaseSettings):
    URL_PREFIX: str = "/api/v1/auth"
    TOKEN_VALIDATE_ENDPOINT: str = "/validate"
    HOST: str
    PORT: int

    class Config:
        env_file = "./.env"


project_config = ProjectModel()
redis_config = RedisModel()
elastic_config = ElasticModel()
auth_config = AuthModel()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
