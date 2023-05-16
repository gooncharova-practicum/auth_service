from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class AppConfig(BaseSettings):
    TESTS_HOST: str
    PORT: int

    class Config:
        env_file = "./.env"


app_config = AppConfig()

API_URL = "/api/v1"
BASE_URL = f"http://{app_config.TESTS_HOST}:{app_config.PORT}{API_URL}"

EXPECTED_RESPONSE_DIR = Path("testdata/expected_response")
