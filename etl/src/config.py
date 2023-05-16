import os

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()


class PgDsn(BaseSettings):
    ELST_DB_DSN: PostgresDsn

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


batch_size = 10
tries_latency = 0.001
sleep_time = 1
max_waiting_time = 30

scheme_name = "content"

default_modified = "1970-01-01 00:00:00.000+0700"
date_format = "%Y-%m-%d %H:%M:%S.%f%z"

index_name = "movies"

postgres_config = PgDsn()
redis_config = RedisModel()
elastic_config = ElasticModel()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
