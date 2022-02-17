#!/bin/bash
echo Starting Flask example app.
## change dir to where the Flask app is located
cd /var/www/flask
## activate the Python virtual environment created in the same folder
source sabio/bin/activate
## change dir into the Flask app
cd sabio


## run gunicorn, which instantiates and manages Python processes that run the app.py script
## prepending SCRIPT_NAME=/api/v1 implies that the gunicorn process has SCRIPT_NAME in its environment variables and is necessary because NGINX internally redirects there (without this, the Flask app would not respond to requests sent with this prefix) 

## arguments: 
##   -w 1 means Gunicorn will run 1 worker
##   -b 127.0.0.1:8080 means listen to this address (this is localhost, since NGINX is set up as a reverse proxy; the port 8080 is arbitrary (although convention) but needs to match the port NGINX redirects client requests to)
##   app:app specifies that app.py is the script where the Flask app itself is defined
##   --log-level debug is the most verbose logging level
##   --timeout 600 (in seconds) is important, since Gunicorn will kill workers if they take longer than the specified timeout to load; since the sABIO backend caches large data structures on star-up this can take up to 10 minutes
SCRIPT_NAME=/api/v1/ gunicorn -w 1 -b 127.0.0.1:8080 app:app --log-level debug --timeout 600

