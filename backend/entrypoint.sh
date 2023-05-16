#!/bin/bash

echo "Run backend"
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${BACKEND_PORT}