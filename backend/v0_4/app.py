import logging
import os

import json

import flask
from flask import request
from flask import jsonify as flask_jsonify
from flask import Response


import numpy as np
import numpy.random as rand

app = flask.Flask(__name__)
# !!! comment out for production !!!
# app.config["DEBUG"] = True




this_pid = str(os.getpid())
home = "/home/valentin.vogelmann/"
logging.basicConfig(filename=home+f'gunicorn_app_{this_pid}.log', 
		level=logging.DEBUG, format=f'%(process)d %(asctime)s | %(message)s')

logging.debug("")
logging.debug("app.py STARTED!")


from src.datasets import NMvW
from src.results import Result
from src.engines.RandomEnginev0 import RandomEngine, nonce_param, redo_param
from src.engines.ContentLengthEnginev0 import ContentLengthEngine
from src.engines.TypicalityEnginev0 import TypicalityEngine

logging.debug("MODULES LOADED!")
logging.debug(f"{NMvW}")



datasets = {NMvW.id:NMvW}

logging.debug(f"{datasets}")
random_engine = RandomEngine(id_="RandomEnginev0",
                           name="RandomEngine/v0",
                           dataset=NMvW,
                           params=[nonce_param, redo_param])
logging.debug("RANDOM ENGINE LOADED!")


cl_engine = ContentLengthEngine(id_="ContentLengthEnginev0",
                            name="ContentLengthEngine/v0",
                            dataset=NMvW,
                            params=[],
                            cached=True)
logging.debug("CONTENT LENGTH ENGINE LOADED!")


#typicality_engine = TypicalityEngine(id_="TypicalityEnginev0",
#                                      name="TypicalityEngine/v0",
#                                      dataset=NMvW,
#                                      params=[])
data_dir = "/data/"
typicality_engine = TypicalityEngine.from_saved(data_dir+"TypicalityEnginev0.pkl")
logging.debug("TYPICALITY ENGINE LOADED!")


# Dictionary of engines
engines = {random_engine.id: random_engine, 
            typicality_engine.id: typicality_engine,
            cl_engine.id: cl_engine}


for eng_name, eng in engines.items():
    for d_id, d in datasets.items():
        d.add_engine(eng)




#def jsonify(data):
#    response = flask_jsonify(data)
#    response.headers.add('Access-Control-Allow-Origin', '*')
#    return response


def jsonify(data):
    data_json = json.dumps(data)
    response = Response(response=data_json, status=200, mimetype="application/json")
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


    scores, details = eng.score_and_detail(relevant_data, **engine_params)

    
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
    detail = d.detail_object(objectID)
    return jsonify(detail)


# def _get_example():
#     # get random dataset D
#     d = rand.choice(list(datasets.values()))

#     # get random engine E
#     e = rand.choice(list(engines.values()))

#     # score all o \in D with E
#     scores, details = e.score_and_detail(d.data)

#     # random draw one o from D (based on scores)
#     rand_i = rand.choice(d.object_count, p=scores/scores.sum())
#     o = d.data.iloc[rand_i]
#     s = scores.iloc[rand_i]
#     return d, e, o, s


# def _get_url(cur_d, cur_e, cur_o):
#     object_params = [dict(id=p.id, value="") for p in cur_d.params]
#     engine_id = cur_e.id
#     engine_params = [dict(id=ep.id, value=ep.default) for ep in cur_e.params]
    



# @app.route("/examples", methods=["GET"])
# def get_examples():
#     n = 4
#     examples = []
#     for i in range(n):
#         cur_d, cur_e, cur_o, cur_s = _get_example()
#         examples.append({
#             "score": cur_s,
#             "title": cur_o.Title,
#             "engine": cur_e.name,
#             "url": ,
#             "thumbnail_url": cur_d.image_source.get_thumb(cur_o.name),
#         })
    
#     return examples
        
        
    
    
    
#     d = list(datasets.values())[0]
#    eng = list(engines.values())[0]
   
#    subsample = d.sample(frac=0.1)
#    scores = eng.score(subsample)
   
#    highest_inds = np.argsort(scores)[-10:]
#    examples = subsample.iloc[highest_inds]
#    example_scores = scores[highest_inds]
    
#     dicts = [
    


# !!! comment out for production !!!
# if __name__ == "__main__":
#     app.run()

        
        
        
        
        
        
        
        
        
# /browse/{cur_d}/
 
# + 
#         urlencode(
#     json(
        
# {
#     'objectKeywords': "", # empty
#     'objectStartDate': "", # empty
#     'objectEndDate': "", # empty
#     'objectParams': "", # empty = default?
#     'engineId': cur_e.id, 
#     'engineMinScore': cur_e.min_score, 
#     'engineMaxScore': cur_e.max_score, # doesn't exist
#     'engineParams': "", #empty 
#     'vocabularyTerms': "" # not sure - empty?
# }
#     )
# )
        
# +
        
#         scatterplot/


# 0/  <-- what is this?


# {cur_o.ObjectID}?api=https://sabio.diginfra.nl/api/v1/
        
# https://sabio.sudox.nl/browse/openimages/%7B%22objectKeywords%22%3A%22politionele%22%2C%22objectStartDate%22%3A%22%22%2C%22objectEndDate%22%3A%221960-04-09%22%2C%22objectParams%22%3A[%7B%22id%22%3A%22location%22%2C%22value%22%3A%22%22%7D%2C%7B%22id%22%3A%22subject%22%2C%22value%22%3A%22%22%7D%2C%7B%22id%22%3A%22type%22%2C%22value%22%3A%22%22%7D%2C%7B%22id%22%3A%22publisher%22%2C%22value%22%3A%22%22%7D]%2C%22engineId%22%3A%22word-match%22%2C%22engineMinScore%22%3A0.075%2C%22engineMaxScore%22%3A0.5650000000000001%2C%22engineParams%22%3A[%7B%22id%22%3A%22score_name%22%2C%22value%22%3A%226%22%7D%2C%7B%22id%22%3A%22score_description%22%2C%22value%22%3A%222%22%7D]%2C%22vocabularyTerms%22%3A%22bewindhebber%2Cbewindvoerder%2Cbomba%2Cbombay%2Ccimarron%2Cderde%20wereld%2Cdwerg%2Cexpeditie%2Cgouverneur%2Chalfbloed%2Chottentot%2Cinboorling%2Cindiaan%2Cindisch%2Cindo%2Cinheems%2Cinlander%2Cjap%2Cjappen%2Cjappenkampen%2Ckaffer%2Ckaffir%2Ckafir%2Ckoelie%2Ckolonie%2Clagelonenland%2Clandhuis%2Cmarron%2Cmarronage%2Cmissie%2Cmissionaris%2Cmoor%2Cmoors%2Cmoren%2Cmulat%2Coctroon%2Contdekken%2Contdekking%2Contdekkingsreis%2Contwikkelingsland%2Coorspronkelijk%2Coosters%2Copperhoofd%2Cori%C3%ABntaals%2Cpinda%2Cpolitionele%20actie%2Cprimitief%2Cprimitieven%2Cpygmee%2Cras%2Crasch%2Cslaaf%2Cstam%2Cstamhoofd%2Ctraditioneel%2Ctropisch%2Cwesters%2Cwilden%2Czendeling%2Czendelingen%2Czending%22%7D/scatterplot/0/1186768?api=https%3A%2F%2Fsabio.sudox.nl%2Fapi%2Fv1%2F





# https://sabio.sudox.nl/browse/openimages/{"objectKeywords":"politionele","objectStartDate":"","objectEndDate":"1960-04-09","objectParams":[{"id":"location","value":""},{"id":"subject","value":""},{"id":"type","value":""},{"id":"publisher","value":""}],"engineId":"word-match","engineMinScore":0.075,"engineMaxScore":0.5650000000000001,"engineParams":[{"id":"score_name","value":"6"},{"id":"score_description","value":"2"}],"vocabularyTerms":"bewindhebber,bewindvoerder,bomba,bombay,cimarron,derde wereld,dwerg,expeditie,gouverneur,halfbloed,hottentot,inboorling,indiaan,indisch,indo,inheems,inlander,jap,jappen,jappenkampen,kaffer,kaffir,kafir,koelie,kolonie,lagelonenland,landhuis,marron,marronage,missie,missionaris,moor,moors,moren,mulat,octroon,ontdekken,ontdekking,ontdekkingsreis,ontwikkelingsland,oorspronkelijk,oosters,opperhoofd,oriëntaals,pinda,politionele actie,primitief,primitieven,pygmee,ras,rasch,slaaf,stam,stamhoofd,traditioneel,tropisch,westers,wilden,zendeling,zendelingen,zending"}/scatterplot/0/1186768?api=https://sabio.sudox.nl/api/v1/