import flask
from flask import jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

import numpy as np
from datasets import NMvW
from engines import rand_engine

engine_list = sorted([rand_engine])

dataset_list = sorted([NMvW])

with open("home.html") as handle:
    home_html = handle.read() 


@app.route("/", methods=["GET"])
@app.route("/api/v1/", methods=["GET"])
def home():
    # prepare data here
    return home_html

@app.route("/datasets", methods=["GET"])
def list_datasets():
    return jsonify([d.to_dict() for d in dataset_list])
    

@app.route("/datasets/<datasetID>/autocomplete", methods=["GET"])
def autocomplete(datasetID):
    param_name = request.args["attribute"]
    kw = request.args["keyword"]
    
    d = dataset_list[int(datasetID)]
    try:
        param = d.params[param_name]
    except KeyError:
        raise KeyError(f"There is no DatasetParam {param_name}")
    
    list_of_options = param.autocomplete(d.data, param_name, kw)
    return jsonify(list_of_options)


@app.route("/engines", methods=["GET"])
def get_engines():
    return jsonify([e.to_dict() for e in engine_list])
    
@app.route("/engines/<engineID>/html", methods=["GET"])
def get_engine_detail(engineID):
    cur_engine = engine_list[int(engineID)]
    return cur_engine.summary()


@app.route("/objects/<datasetID>/search", methods=["GET"])
def search_objects(datasetID):
    # object
    kws = request.args["object_keywords"]
    start = request.args["object_start_date"]
    end = request.args["object_end_date"]
    obj_params = [a for a in request.args if a.startswith("object_param_")]
    
    # engine
    engine_id = request.args["engine_id"]
    engine_min = request.args["engine_min_score"]
    engine_max = request.args["engine_max_score"]
    engine_params = [a for a in request.args if a.startswith("engine_param_")]
    
    #vocabulary
    vocab = request.args["vocabulary_terms"]
    
    # produces list of Result
    
    print(type(request.args))
    return jsonify(request.args)
    
    
@app.route("/objects/<datasetID>/details/<objectID>", methods=["GET"])
def get_object_details(datasetID, objectID):
    d = dataset_list[int(datasetID)]
    rand_id = np.random.choice(d.objectIDs)
    return jsonify(d.get_object(rand_id)) # ATTENTION: random ID


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
