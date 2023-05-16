from logging import getLogger
from time import sleep

import aioredis

from config import batch_size, redis_config, tries_latency, sleep_time
from state_saver import RedisStorage, State
from tools import transformator_pg_es

logger = getLogger()
redis = aioredis.from_url(
    f"redis://{redis_config.REDIS_HOST}:{redis_config.REDIS_PORT}"
)
state = State(RedisStorage(redis))

shorts_list = ["fw", "g", "p", "genres_only", "persons_only"]


def main():
    while True:
        for obj in shorts_list:
            logger.info(f"Operation with {obj} started")
            transformator_pg_es(obj, batch_size, state, tries_latency)
            logger.info(f"Operation with {obj} ended")
        sleep(sleep_time)


if __name__ == "__main__":
    main()
