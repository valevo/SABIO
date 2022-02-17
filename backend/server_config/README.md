# Server Config Instructions & Files

SABIO's backend is a `Python Flask` application that uses `NGINX` as reverse-proxy and `Gunicorn` as WSGI HTTP server. It has been developed on a `Ubuntu 20.04.3 LTS` server.

Requirements, installation instructions and configuration files can be found in this directory.


# Installation

OS install (self-standing applications; used Ubuntu's `apt` package manager):

 - `nginx`
 - `certbot` (sets up certificates for HTTPS, incl redirect in the NGINX config; followed the [`certbot` installation instructions](https://certbot.eff.org/instructions?ws=nginx&os=ubuntuxenial) for NGINX + Ubuntu 20) -- NB: certbot requires the HTTP server to be already installed and configured (as it needs to change that configuration))

Python install (used Python's `pip3`):

 - `gunicorn`
 - `flask`
 - `pipenv`
 - other required Python packages -> see requirements.txt



Need to create a virtual environment in the directory `/var/www/flask/sabio/` 
(with `python -m venv /var/www/flask/sabio/`)


# Files in this directory

 - `flask.service`: defines a service for the Flask app (actually for Gunicorn, which is responsible for starting Python workers),  
   located in `/lib/systemd/system/`,
   service can then be started/monitored/stopped with `(sudo) systemctl start/status/stop flask`

 - `nginx.service`: defines a service for the NGINX reverse-proxy server, located in `/lib/systemd/system/`,  
    service can then be started/monitored/stopped with `(sudo) systemctl start/status/stop nginx`, this file is  
    automatically created when installing NGINX (not manually modified)


 - `reverse-proxy.conf`: the config file for the NGINX reverse-proxy server, located in `/etc/nginx/sites-enabled/`
   
 - `start.sh`: executed by `flask.service` (this bash script actually runs `gunicorn`), 
    located in `/var/www/flask/sabio/`, activates the Python virtual environment and runs `gunicorn` with 
    the Python script `app.py` and appropriate parameters




# Useful Tutorials

list of Flask/Gunicorn/Nginx setup tutorials that were followed to create the SABIO backend; needed to diverge from their instructions a number of times but they might still be helpful references (and explain some configurations in more detail):

 - [basic introdfuction to building a Flask app](https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask)


 - [instructions on deploying a Flask app with Gunicorn and NGINX](https://dev.to/brandonwallace/deploy-flask-the-easy-way-with-gunicorn-and-nginx-jgc); mainly followed this one

 - [DigitalOcean: how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)
 
 - [Nginx tutorial](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy) that could help figure out how to set an internal redirect from / to /api/v0
 
  - [NGINX Config Pitfalls](https://www.nginx.com/resources/wiki/start/topics/tutorials/config_pitfalls/) -- a list of problems and bad practices
  
 - [instructions how to do NGINX with Certbot](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04)
 
<!--   - [Example NGINX config for Gunicorn](https://docs.gunicorn.org/en/stable/deploy.html) -> could be more efficient & more stable & more secure
 - [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/index.html0) -> alternative to Gunicorn? -->

