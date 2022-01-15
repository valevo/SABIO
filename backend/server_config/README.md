# Server Config Instructions & Files

The SABIO backend server has been developed on `Ubuntu 20.04.3 LTS`.

It is a `Python Flask` application that uses `NGINX` as reverse-proxy and `Gunicorn` as WSGI HTTP server.

Requirements, installation instructions and configuration files can be found in this directory.


# Installation

OS install (self-standing applications, used Ubuntu's `apt` package managing tool):

 - nginx

Python install (used Python `pip`):

 - `gunicorn`
 - `flask`
 - other required Python packages -> see requirements.txt



Need to create a viratual environment in the directory `/var/www/flask/sabio/` 
(with `python -m venv `/var/www/flask/sabio/`)


# Files in this directory

 - `flask.service`: defines a service for the Flask app (actually for Gunicorn, which is responsible for 
    starting Python workers), located in `/lib/systemd/system/`, 
    service can then be started/monitored/stopped with `(sudo) systemctl start/status/stop flask`

 - `nginx.service`: defines a service for the NGINX reverse-proxy server, located in `/lib/systemd/system/`,
    service can then be started/monitored/stopped with `(sudo) systemctl start/status/stop nginx`, this file is
    automatically created when installing NGINX (not manually modified)


 - `reverse-proxy.conf`: the cofig file for the NGINX reverse-proxy server, located in `/etc/nginx/sites-enabled/`
   
 - `start.sh`: executed by `flask.service` (this bash script actually runs `gunicorn`), 
    located in `/var/www/flask/sabio/`, activates the Python virtual environment and runs `gunicorn` with 
    the Python script `app.py` and appropriate parameters
