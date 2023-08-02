# Specs and requirements for a server to run SABIO (as is)

# Prelims

 - SABIO is a 'Flask' application (Python library for handling requests), configured to
   listen to requests at localhost (127.0.0.1)

 - SABIO is a static application, i.e. client-side requests do not alter any files on the server
   (i.e. not user-database, no collection of data of any kind, etc)
   => system requirements (hard- and software) do not change; maintenance minimal


 - the number of worker Python processes that gunicorn (WSGI app) starts
   => each worker occupies roughly the same amount of RAM
   => more workers can handle more simultaneous requests (distribution done by gunicorn), for now one worker 
      is probably enough


# Hardware

(with NMvW/v0 and OpenBeelden datasets added to SABIO)

 - SABIO Python process occupies around 5GB of RAM


# Software
