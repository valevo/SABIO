# import sys
# print(sys.path)
# sys.path.insert(0, "/home/valentin/Desktop/SABIO_docker/src/")
# print(sys.path)



from tqdm import tqdm
tqdm.pandas()
import json
from urllib.parse import quote

import numpy as np
import numpy.random as rand

import flask
from flask import request
from flask import jsonify as flask_jsonify
from flask import Response

# import numpy as np
# import numpy.random as rand

app = flask.Flask(__name__)
# !!! comment out for production !!!
app.config["DEBUG"] = True

from datasets import NMvW, OpenBeelden
from results import Result
from engines.RandomEnginev0 import RandomEngine, nonce_param, redo_param
from engines.ContentLengthEnginev0 import ContentLengthEngine
from engines.VocabularyEnginev0 import VocabularyEngine
from engines.TypicalityEnginev0 import TypicalityEngine
from engines.PMIEnginev0 import PMIEngine



from tqdm import tqdm

cache_dir = "../cache"

datasets = {
            NMvW.ID: NMvW, 
            OpenBeelden.ID: OpenBeelden
}


random_engine = RandomEngine(ID="RandomEnginev0",
                            name="RandomEngine/v0",
                            params=[nonce_param, redo_param],
                            cache_dir=cache_dir)

CL_engine = ContentLengthEngine(ID="ContentLengthEnginev0",
                            name="ContentLengthEngine/v0",
                            params=[],
                            cache_dir=cache_dir)

vocab_engine = VocabularyEngine(ID="VocabularyEnginev0",
                                name="VocabularyEngine/v0",
                                params=[],
                                cache_dir=cache_dir)

typ_engine = TypicalityEngine(ID="TypicalityEnginev0",
                                name="TypicalityEngine/v0",
                                params=[],
                                cache_dir=cache_dir)

pmi_engine = PMIEngine(ID="PMIEnginev0",
                                name="PMIEngine/v0",
                                params=[],
                                cache_dir=cache_dir)


engines = [random_engine, 
           CL_engine, 
           vocab_engine, 
           typ_engine,
            pmi_engine]
engines = {e.ID: e for e in engines}

# CACHE SCORES FOR ALL DATASETS
# -> put into a separate script/function (doesn't need to happen at startup of Flask app)
for e_ID, e in engines.items():
    for d_ID, d in datasets.items():
        # if isinstance(e, CachedEngine):  # check to make start-up faster -> non-cached engines are fast anyway
        e.score_and_detail(dataset=d, indices=d.index)
        d.add_engine(e)
    
    

    
def jsonify(data):
    data_json = json.dumps(data)
    response = Response(response=data_json, status=200, mimetype="application/json")
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
    return jsonify([e.to_dict() for e_ID, e in sorted(engines.items())])


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
    obj_params = {a.replace("object_param_", ""): val for a, val in request.args.items()
                  if a.startswith("object_param_")}
    
    
     # engine
    engine_id = request.args["engine_id"]
    engine_min = float(request.args["engine_min_score"])
    engine_max = float(request.args["engine_max_score"])
    engine_params = {a.replace("engine_param_", ""): val for a, val in request.args.items()
                     if a.startswith("engine_param_")}
    
    # vocabulary
    vocab = request.args["vocabulary_terms"]
    engine_params.update(dict(vocabulary=vocab))

    
    d = datasets[datasetID]
#     logging.debug(f"received: {datasetID}\nretrieved: {d}\n params: {obj_params}")
    eng = engines[engine_id]


    
    #################################################################
    ### COMPUTE RESPONSE ############################################

    # search 
    relevant_indices = d.search(kws, start, end,
                                 indices_only=True,
                                 **obj_params)
    relevant_data = d.data.loc[relevant_indices]
    
    scores, details = eng.score_and_detail(d, relevant_indices,
                                           **engine_params)

    
    # filter objects based on score and min_score and max_score parameters
    # (i.e. only keep objects whose is between min_score and max_score)
    # min_score and max_score sent be y the front end are in [0.0, 1.0]
    in_score_rng = (engine_min <= scores) & (scores <= engine_max)
    filtered_scores = scores[in_score_rng]
    filtered_details = details[in_score_rng]
    filtered_data = relevant_data[in_score_rng]

    
    thumbnails = d.image_source.get_thumb(filtered_data.index)
    
    # instantiate Result object 
    # TODO? let result object do filtering of objects above
    # NOW: Result object is responsible for formatting
    param_names = list(d.params.keys())
    results = Result(param_names, filtered_data, filtered_scores, filtered_details,
                    engine_min, engine_max, thumbnails)
    
    # produces list of Result
    return jsonify(results.to_dict())


@app.route("/objects/<datasetID>/details/<objectID>", methods=["GET"])
def get_object_details(datasetID, objectID):
    d = datasets[datasetID]
    detail = d.detail_object(int(objectID))
    return jsonify(detail)




### EXAMPLES
def _get_example():
    # get random dataset D
    d = rand.choice(list(datasets.values()))

    # get random engine E
#     fast_engines = {k: v for k, v in engines.items() if not "vocabulary" in k.lower()}
    e = rand.choice(list(engines.values()), replace=False)

    # score all o \in D with E
    param_dict = {}  # param_dict = dict(constant_scores=True)
    scores, details = e.score_and_detail(d, d.index, **param_dict)

    # filter out scores not in value range given by engine (!: need to be >=0 for andom choice below)
    # <= e.max_score technically not necessary, BUT ADD BACK IN
    in_score_rng = (e.min_score <= scores) # & (scores <= e.max_score)
    filtered_scores = scores[in_score_rng]
    filtered_data = d.data[in_score_rng]

    def norm(ls):
        a = np.asarray(ls)
        return a/a.sum()
    
    # random draw one o from D (based on scores)
    rand_i = rand.choice(len(filtered_data.index), 
                         p=norm(norm(filtered_scores)**3))
    o = filtered_data.iloc[rand_i]
    s = filtered_scores.iloc[rand_i]
    return d, e, o, s


def _get_url(cur_d, cur_e, cur_o):
    # construct Object param dicts with empty values 
    object_params = [dict(id=p_id, value="") for p_id, p in cur_d.params.items()]
    # construct Engine param dicts with default values
    engine_params = [dict(id=ep.ID, value=ep.default) for ep in cur_e.params]
    
    
    vocab = cur_e.re2vocab(cur_e.all_examples) if isinstance(cur_e, VocabularyEngine) else ""
    param_dict = {
            'objectKeywords': "", # empty
            'objectStartDate': "", # empty
            'objectEndDate': "", # empty
            'objectParams': object_params, # empty = default?
            'engineId': cur_e.ID, 
            'engineMinScore': cur_e.min_score,
            'engineMaxScore': cur_e.max_score,
            'engineParams': engine_params, # defaults
            'vocabularyTerms': vocab  # vocab_engine.all_examples.pattern.replace("|", ",").replace(r"\b", "")
        }
    
    param_dict = quote(json.dumps(param_dict), safe="")
    api = quote("https://sabio.diginfra.net/api/v1/", safe="")
    view, attribute = "scatterplot", "0"
    
    cur_ObjectID = cur_o.name
    return f"/browse/{cur_d.ID}/{param_dict}/{view}/{attribute}/{cur_ObjectID}?api={api}"



@app.route("/examples", methods=["GET"])
def get_examples():
    n = 4
    examples = []
    for i in range(n):
        print(f"loop {i}")
        cur_d, cur_e, cur_o, cur_s = _get_example()
        print("_get_example() done")
        examples.append({
            "score": cur_s,
            "title": cur_o["name"],
            "engine": cur_e.name,
            "url": _get_url(cur_d, cur_e, cur_o),
            "thumbnail_url": cur_d.image_source.get_thumb(cur_o.name),
        })
        print("example costructed")
    
    return jsonify({"examples": examples})


if __name__ == "__main__":
	app.run(debug=True)

    
    
    
# http://127.0.0.1:5000/objects/NMvW_v0/search?object_keywords=&object_start_date=&object_end_date=&engine_id=TypicalityEnginev0&engine_min_score=0&engine_max_score=1&vocabulary_terms=bewindhebber%2Cbewindvoerder%2Cbomba%2Cbombay%2Ccimarron%2Cderde%20wereld%2Cdwerg%2Cexpeditie%2Cgouverneur%2Chalfbloed%2Chottentot%2Cinboorling%2Cindiaan%2Cindisch%2Cindo%2Cinheems%2Cinlander%2Cjap%2Cjappen%2Cjappenkampen%2Ckaffer%2Ckaffir%2Ckafir%2Ckoelie%2Ckolonie%2Clagelonenland%2Clandhuis%2Cmarron%2Cmarronage%2Cmissie%2Cmissionaris%2Cmoor%2Cmoors%2Cmoren%2Cmulat%2Coctroon%2Contdekken%2Contdekking%2Contdekkingsreis%2Contwikkelingsland%2Coorspronkelijk%2Coosters%2Copperhoofd%2Cori%C3%ABntaals%2Cpinda%2Cpolitionele%20actie%2Cprimitief%2Cprimitieven%2Cpygmee%2Cras%2Crasch%2Cslaaf%2Cstam%2Cstamhoofd%2Ctraditioneel%2Ctropisch%2Cwesters%2Cwilden%2Czendeling%2Czendelingen%2Czending&object_param_Classification=&object_param_Department=
    
    
    
