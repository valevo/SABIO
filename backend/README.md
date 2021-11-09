# SABIO_backend
SABIO webapp code for sharing between server and local machine



## Process

### NMvW Data:




### Server Setup

 - [Nginx+Gunicorn+Flask](https://dev.to/chand1012/how-to-host-a-flask-server-with-gunicorn-and-https-942), uses reverse-proxy, i.e. Gunicorn listens on localhost, Nginx forwards to localhost

 - [Nginx tutorial](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy) that could help figure out how to set an internal redirect from / to /api/v0

 - CORS (Cross Origin Resource Sharing)
 - [Certbot](https://certbot.eff.org/lets-encrypt/ubuntufocal-nginx)




# TODO 
 
 - precompute results for presets of parameters
 - 
 - hard cap:
   - for long texts at 1000 characters
   - for long titles at 100 characters



# Ideas

 - new engine: 'lack of information' engine -> e.g. computes the ratio of fields missing
 - typicality engine: compute objects' typicality as a proxy for how 'common' a certain description








### Things to Potentially Check


 - [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/index.html0) -> alternative to Gunicorn?

 - [Example NGINX config for Gunicorn](https://docs.gunicorn.org/en/stable/deploy.html) -> could be more efficient & more stable & more secure

 - [Nginx Config Pitfalls](https://www.nginx.com/resources/wiki/start/topics/tutorials/config_pitfalls/), random list of problems and bad practices

 - [instructions how to do Nginx with Certbot](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04) -> also has instructions how to configure firewall etc





