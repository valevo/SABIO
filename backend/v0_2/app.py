import flask
from flask import request
from flask import jsonify as flask_jsonify


app = flask.Flask(__name__)
app.config["DEBUG"] = True

# from werkzeug.middleware.profiler import ProfilerMiddleware
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




def jsonify(data):
    response = flask_jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


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
    results = Result(filtered_data, filtered_scores, filtered_details,
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
    
    dicts = [{"title": r.Title,
              "score": s,
              "thumbnail_url": ,
              "engine": eng,
              "url": ,
    
              
"""https://sabio.sudox.nl/browse/openimages/%7B%22objectKeywords%22%3A%22%22%2C%22objectStartDate%22%3A%22%22%2C%22objectEndDate%22%3A%22%22%2C%22objectParams%22%3A[%7B%22id%22%3A%22location%22%2C%22value%22%3A%22%22%7D%2C%7B%22id%22%3A%22subject%22%2C%22value%22%3A%22%22%7D%2C%7B%22id%22%3A%22type%22%2C%22value%22%3A%22%22%7D%2C%7B%22id%22%3A%22publisher%22%2C%22value%22%3A%22%22%7D]%2C%22engineId%22%3A%22word-match%22%2C%22engineMinScore%22%3A0%2C%22engineMaxScore%22%3A0.5650000000000001%2C%22engineParams%22%3A[%7B%22id%22%3A%22score_name%22%2C%22value%22%3A%226%22%7D%2C%7B%22id%22%3A%22score_description%22%2C%22value%22%3A%222%22%7D]%2C%22vocabularyTerms%22%3A%22africa%2Cafrika%2Callada%2Caneho%2Cangola%2Cannobon%2Cantongil%20baai%2Cappa%2Carguin%2Caruba%2Catjeh%2Caxim%2Cbadagri%2Cbali%2Cbanda%2Cbanda%20eilanden%2Cbangladesh%2Cbantam%2Cbantan%2Cbanten%2Cbarbados%2Cbatavia%2Cbengalen%2Cbenin%20city%2Cberbice%2Cbonaire%2Cborneo%2Cbrasil%2Cbrazili%C3%AB%2Ccasteel%20del%20mina%2Cceylon%2Ccolombo%2Ccormant%2Ccormantijn%2Ccormantin%2Ccoromandel%2Ccura%C3%A7ao%2Cdejima%2Cdelagoa%2Cdemerara%2Cdemerary%2Cd%E2%80%99elmina%2Celmina%2Cepe%2Cepk%C3%A9%2Cessequebo%2Cessequibo%2Cformosa%2Cfort%20amsterdam%2Cfort%20cormantijn%2Cfort%20cormantin%2Cfort%20gor%C3%A9e%2Cfort%20kormantijn%2Cfort%20kormantin%2Cfort%20nassau%2Cfort%20nieuw%20amsterdam%2Cfort%20oranje%2Cfort%20zeelandia%2Cfort%20zelandia%2Cghana%2Cgoeree%2Cgor%C3%A9e%2Cgoudkust%2Cgrand-popo%2Cgreijn%2Cgrein%2Cgrijn%2Cguiana%2Cguinea%2Cguinee%2Cguyana%2Ch%C3%B4i%20an%2Cindia%2Cindische%2Cindi%C3%AB%2Cindonesi%C3%AB%2Cjaquim%2Cjava%2Ckaap%2Ckaapkolonie%2Ckongo%2Ckormant%2Ckormantijn%2Ckormantin%2Cloanga%2Cmadagaskar%2Cmakassa%2Cmalabar%2Cmalakka%2Cmalediven%2Cmeidorp%2Fmeiborg%2Cmina%2Cmolukken%2Cmorenland%2Cnederlands%20ceylon%2Cnederlands%20guiana%2Cnederlands%20nieuw%20guinea%2Cnederlands-brazili%C3%AB%2Cnederlands-indi%C3%AB%2Cnederlandse%20antillen%2Cnieuw%20amsterdam%2Cnieuw-nederland%2Coffra%2Couidah%2Cpapoea%2Cpapua%2Cparamaribo%2Cpenghu%20eilanden%2Cpernambuco%2Cpescadorus%2Cprincipe%2Csaba%2Csao%20tom%C3%A9%2Csave%2Csint%20eustatius%2Csint%20jago%2Csint%20maarten%2Csint%20thomas%2Cslavenkust%2Cst.%20eustatius%2Cst.%20jago%2Cst.%20maarten%2Cst.%20thomas%2Cstabroek%2Csumatra%2Csurat%2Csuriname%2Ctandkust%2Ctobago%2Ctogo%2Ctonkin%2Cwest-indische%2Cwest-indi%C3%AB%2Cwillemstad%2Czuid-afrika%22%7D/scatterplot/0/1231179?api=https%3A%2F%2Fsabio.sudox.nl%2Fapi%2Fv1%2F"""
    
    
    


# # COMMENT OUT FOR PRODUCTION
if __name__ == "__main__":
    app.run()