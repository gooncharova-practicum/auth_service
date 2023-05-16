#!/bin/bash

echo "Running auth service"
gunicorn --workers=2 'app:create_app()' --preload --bind ${HOST}:${PORT}