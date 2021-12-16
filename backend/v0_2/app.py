import flask
from flask import request
from flask import jsonify as flask_jsonify


app = flask.Flask(__name__)
# !!! comment out for production !!!
#app.config["DEBUG"] = True

# from werkzeug.middleware.profiler import ProfilerMiddleware
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir="./profiles/")


import logging
import os

this_pid = str(os.getpid())
logging.basicConfig(filename=f'/home/valentin.vogelmann/gunicorn_app_{this_pid}.log', level=logging.DEBUG, format=f'%(process)d %(asctime)s | %(message)s')


import numpy as np
# from src.datasets import Dataset, Result, df, NMvW_params
from src.datasets import NMvW
from src.results import Result
from src.engines.RandomEnginev0 import RandomEngine, nonce_param

logging.debug("MODULES LOADED!")
logging.debug(f"{NMvW}")



datasets = {NMvW.id:NMvW}

logging.debug(f"{datasets}")
random_engine = RandomEngine(id_="RandomEnginev0",
                           name="RandomEngine/v0",
                           dataset=NMvW,
                           params=[nonce_param])

logging.debug("RANDOM ENGINE LOADED!")


# Dictionary of engines
engines = {random_engine.id: random_engine}

print(engines[random_engine.id].description())

for eng_name, eng in engines.items():
    for d_id, d in datasets.items():
        d.add_engine(eng)


print(datasets[NMvW.id])



def jsonify(data):
    response = flask_jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/", methods=["GET"])
def home():
    return jsonify(["hello world"])

@app.route("/datasets", methods=["GET"])
def list_datasets():
    return jsonify([d.to_dict() for i, d in sorted(datasets.items())])



@app.route("/datasets/<datasetID>/autocomplete", methods=["GET"])
def autocomplete(datasetID):
    param_id = request.args["param"]
    kw = request.args["keyword"]
    
    d = datasets[datasetID]
    try:
        param = d.params[param_id]
    except KeyError:
        raise KeyError(f"There is no DatasetParam with ID <{param_id}>")
    
    list_of_options = param.autocomplete(d.data, kw)
    
    return jsonify(list_of_options)


@app.route("/engines", methods=["GET"])
def get_engines():
    return jsonify([e.to_dict() for e_id, e in sorted(engines.items())])



@app.route("/engines/<engineID>/html", methods=["GET"])
def get_engine_detail(engineID):
    cur_engine = engines[engineID]
    return cur_engine.description()



@app.route("/objects/<datasetID>/search", methods=["GET"])
def search_objects(datasetID):
    ### GATHER PARAMETERS ##########################################
    # object
    kws = request.args["object_keywords"]
    start = request.args["object_start_date"]
    end = request.args["object_end_date"]
    obj_params = {a.replace("object_param_", ""): val for a, val in request.args.items() if a.startswith("object_param_")}
    
    
    # engine
    engine_id = request.args["engine_id"]
    engine_min = float(request.args["engine_min_score"])
    engine_max = float(request.args["engine_max_score"])
    engine_params = {a.replace("engine_param_", ""): val for a, val in request.args.items() if a.startswith("engine_param_")}
    
    
    # vocabulary
    vocab = request.args["vocabulary_terms"]

    
    d = datasets[datasetID]
    eng = engines[engine_id]

    #################################################################
    ### COMPUTE RESPONSE ############################################

    # search 
    relevant_data = d.search(kws, start, end, **obj_params)

    # score
    scores = eng.score(relevant_data, **engine_params)
    # score details
    details = eng.score_details(relevant_data, **engine_params)

    
    # filter objects based on score and min_score and max_score parameters
    # (i.e. only keep objects whose is between min_score and max_score)
    in_score_rng = (engine_min <= scores) & (scores <= engine_max)
    filtered_scores = scores[in_score_rng]
    filtered_details = details[in_score_rng]
    filtered_data = relevant_data[in_score_rng]

    # instantiate Result object 
    # TODO? let result object do filtering of objects above
    # NOW: Result object is responsible for formatting
    param_names = d.params.keys()
    logging.debug(f"SEARCH_OBJECTS {param_names}: {d.params}")
    results = Result(param_names, filtered_data, filtered_scores, filtered_details,
                    engine_min, engine_max)
    
    # produces list of Result
    return jsonify(results.to_dict())




@app.route("/objects/<datasetID>/details/<objectID>", methods=["GET"])
def get_object_details(datasetID, objectID):
    d = datasets[datasetID]
    detail = d.detail_object(objectID)
    return jsonify(detail)


@app.route("/examples", methods=["GET"])
def get_examples():
    d = list(datasets.values())[0]
    eng = list(engines.values())[0]
    
    subsample = d.sample(frac=0.1)
    scores = eng.score(subsample)
    
    highest_inds = np.argsort(scores)[-10:]
    examples = subsample.iloc[highest_inds]
    example_scores = scores[highest_inds]
    
#     dicts = [{"title": r.Title,
#               "score": s,
#               "thumbnail_url": ,
#               "engine": eng,
#               "url": ,

    
    


# !!! comment out for production !!!
#if __name__ == "__main__":
#    app.run()
