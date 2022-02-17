# SABIO_backend
SABIO webapp code for sharing between server and local machine


# IMPORTANT

### From Dev to Production

 - in app.py: remove `app.config["DEBUG"] = True` and `if __name__ == "__main__":
    app.run()`




## Process

### NMvW Data:




### Server Setup

 - [Nginx tutorial](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy) that could help figure out how to set an internal redirect from / to /api/v0




# TODO 
 
 
 
 
 - hard cap:
   - for long texts at 1000 characters
   - for long titles at 100 characters

 - add logging of backend activities
 - store searches (&results) locally



# Ideas

 - new engine: 'lack of information' engine -> e.g. computes the ratio of fields missing

