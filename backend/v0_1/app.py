import flask
from flask import request
from flask import jsonify as flask_jsonify

from werkzeug.middleware.profiler import ProfilerMiddleware

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir="./profiles/")


import numpy as np
from src.datasets import Dataset, Result, df, NMvW_params
from src.engines import RandomEngine, nonce_param


NMvW = Dataset(df, "NMvW_v0", 
               "Nationaal Museum van Wereldculturen 1M",
               "https://collectie.wereldculturen.nl/",
               NMvW_params,
               available_engines=[])
datasets = {NMvW.id:NMvW}


rand_engine = RandomEngine(id_="RandE_v0", 
                           name="RandomEngine/v1.0",
                           dataset=NMvW,
                           params=[nonce_param])
engines = {rand_engine.id: rand_engine}
NMvW.add_engine(rand_engine)




with open("src/home.html") as handle:
    home_html = handle.read() 


def jsonify(data):
    response = flask_jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route("/", methods=["GET"])
# @app.route("/api/v1/", methods=["GET"])
def home():
    # prepare data here
    return home_html

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
    return cur_engine.summary()


@app.route("/objects/<datasetID>/search", methods=["GET"])
def search_objects(datasetID):
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
    
    #vocabulary
    vocab = request.args["vocabulary_terms"]
    
    
    ## compute response
    
    d = datasets[datasetID]
    
    relevant_data = d.search(kws, start, end, **obj_params)
    
    
    eng = engines[engine_id]

    scores = eng.score(relevant_data, **engine_params)
    details = eng.score_details(relevant_data, **engine_params)

#     details = np.asarray(["{}"]*relevant_data.shape[0])
    
    in_score_rng = (engine_min <= scores) & (scores <= engine_max)
    
    filtered_scores = scores[in_score_rng]
    filtered_details = details[in_score_rng]
    filtered_data = relevant_data[in_score_rng]

    
    print("\n---------------------------\n")
    print(engine_min, engine_max)
    print(in_score_rng.sum(), np.where(in_score_rng)[0][100:110])
    print(filtered_data)
    print("\n---------------------------\n")
    
    results = Result(filtered_data, filtered_scores, filtered_details,
                    engine_min, engine_max)
    
    # produces list of Result
    return jsonify(results.to_dict())
    
    
@app.route("/objects/<datasetID>/details/<objectID>", methods=["GET"])
def get_object_details(datasetID, objectID):
    d = datasets[datasetID]
    detail = d.detail_object(objectID)
        
    return jsonify(detail)


# # COMMENT OUT FOR PRODUCTION
if __name__ == "__main__":
    app.run()
