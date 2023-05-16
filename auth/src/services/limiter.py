from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from src.core import base_config, redis_config

limiter = Limiter(
    get_remote_address,
    default_limits=[base_config.REQUEST_LIMIT],
    storage_uri=redis_config.REDIS_DSN,
)
