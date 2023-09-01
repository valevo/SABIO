#!/bin/bash
echo "Starting Sabio Server"

# Set missing environment variables to default values
: "${LIMIT_REQUIRES_LINE:=8190}"
: "${LOG_LEVEL:=critical}"
: "${PORT:=8080}"
: "${SCRIPT_NAME:=/api/v1/}"
: "${TIMEOUT:=600}"
: "${WORKERS:=2}"

# Go to src directory
cd ./src/

# Start the server with the given parameters:
# --limit-request-line https://docs.gunicorn.org/en/stable/settings.html#limit-request-line -> put that here due to an error encountered once, in which case the request line was 7237
# --timeout 600 required because some engines load large files on startup, which can take up to 5 minutes
# --workers 1 implies that just 1 worker is spawned
gunicorn 'app:app' --bind 0.0.0.0:$PORT --limit-request-line $LIMIT_REQUIRES_LINE --log-level $LOG_LEVEL --timeout $TIMEOUT --workers $WORKERS 
