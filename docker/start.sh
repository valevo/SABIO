#!/bin/bash
echo Starting Flask example app.

cd ./src/
# -w 1 implies that just 1 worker is spawned
# timeout=600 required because some engines load large files on startup, which can take up to 5 minutes
# see https://docs.gunicorn.org/en/stable/settings.html#limit-request-line -> put that here due to an error encountered once, in which case the request line was 7237
SCRIPT_NAME=/api/v1/ gunicorn -w 2 -b 127.0.0.1:8080 'app:app' --log-level debug --timeout 600 --limit-request-line 8190
