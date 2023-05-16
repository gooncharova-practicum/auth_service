#!/usr/bin/env bash

set -e


/opt/app/wait-for-it.sh postgres:${DB_PORT}
/opt/app/wait-for-it.sh redis:${REDIS_PORT}
/opt/app/wait-for-it.sh elastic:${ELASTIC_PORT}

python3 /opt/app/main.py