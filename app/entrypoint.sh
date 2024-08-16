#!/bin/bash

if [ "$DEBUG" = "True" ]; then
    echo "Running in debug mode"
    exec flask run --host=0.0.0.0 --port=8888 --debug
else
    echo "Running in production mode"
    exec gunicorn --bind 0.0.0.0:8888 --workers 4 app:app
fi