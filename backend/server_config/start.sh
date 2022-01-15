#!/bin/bash
echo Starting Flask example app.
cd /var/www/flask
source sabio/bin/activate
cd sabio
#SCRIPT_NAME=/api/v1/ gunicorn -w 4 -b 127.0.0.1:8080 app:app --log-level debug --timeout 120
SCRIPT_NAME=/api/v1/ gunicorn -w 1 -b 127.0.0.1:8080 app:app --log-level debug --timeout 600
