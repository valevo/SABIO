# SABIO

### the [`timeline`](/timeline.md) for Nov & Dec

## guide to [`backend`](/backend)

 - [front-end API specification](/backend/SABIO_API_v0.1.4.yml): Swagger API specification for the frontend written by Werner (upload at https://swagger.io/tools/swagger-editor/ for a nice view)
 - [server configuration files & instructions](/backend/SABIO_API_v0.1.4.yml) used for setting up the SABIO development server (Ubuntu + NGINX)
 - versions [`v0_0`](/backend/v0_0) through [`v0_4`](/backend/v0_4) of the backend which includes the Flask app, helper functionality and the bias scoring engines' definitions


## guide to [`data`](/data)

?



## guide to [`research`](/research)

this folder is where the conceptual and experimental research to build SABIO is recorded (in rather unstructured ways)

 - [ ] [experiments](/experiments): where the different modules that will become SABIO are developed and tested
 - [ ] [resources](/resources): directory with (potentially) relevant papers, websites, external projects, etc.; categorised by field and type 
 - [ ] [theory](/theory): manifesto, ideas for algorithms, conceptual research & constraints from philosophy - information s.t. SABIO fulfills its promise to be a schema for future work 
 - [ ] [inital_plan](/initial_plan.md): the original initial plan for the first steps of SABIO (kept for comparison with what really happened)
 - [ ] [logs](/logs.md): my day-by-day list of notes, pointers and random findings
 - [ ] [mvp](/mvp.md): defining requirements and goals for the Minimal Viable Product, due by July


# Installation

Either follow the Server configuration instructions [here](/backend/server_config/README.md) to setup a (Ubuntu+NGINX) server. Or, if you have a server set up, skip this step and directly set up the SABIO Flask app:

 0. (the Flask app requires a virtual enviroment to be installed in the folder it is served from (otherwise startup scripts will fail))

 1. the app needs to be 'assembled' from the parts in this repository:
   - copy the contents of the latest version in /backend (currently [/backend/v0_4](v0.4)) into the folder you want to serve the Flask app from
   - copy the lastest version of the NMvW data set in /data (currently [/data/v0_2.csv.gz](v0.2)) into {your_path}/NMvW_data/
 
 
 2. in app.py (currently [/backend/v0_4/app.py](v0.4)), there are hard-coded references to directories:
  - home: "/home/valentin.vogelmann/" (this one is just for logging and can be skipped)
  - data_dir: "/data/" (location of pre-cached and saved engines)  
    these references need to be changed to where the 
    
    
 3. 
