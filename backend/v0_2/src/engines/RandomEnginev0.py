import numpy as np
import pandas as pd

from src.engines.engines import Engine, EngineParam



nonce_opts = {"1": "useless1", "2": "useless2"}    
nonce_vals = {k: k for k in nonce_opts}
nonce_param = EngineParam(id_="nonce", label="Nonce Parameter", 
                          description="This parameter has no effect and that is its point.",
                          control="select", default="1",
                          options=nonce_opts,
                         option2value=nonce_vals)

redo_opts = {"True": "yes", "False": "no"}
redo_vals = {"True": True, "False": False} 
redo_param = EngineParam(id_="redo", label="Rescore Parameter",
                         description="Redo the random scoring of the dataset.",
                         control="select", default="False",
                         options=redo_opts,
                        option2value=redo_vals)



class RandomEngine(Engine):
    def __init__(self, **engine_args):
        super().__init__(**engine_args)
        self.min_score = 0. # np.random.random()*100
        
#         self.constant_scores = None
        scores = self.score(self.dataset.data, redo=True)
        self.constant_scores = scores
        
#         self.constant_score_details = None
        self.constant_score_details = self.score_details(self.dataset.data, redo=True)
        
#     def description(self):
#         with open("RandomEngine.v0.html") as handle:
#             html = handle.read()
#         with open("descriptions.css") as handle:
#             css = handle.read()
        
#         html.replace("<style></style>",
#                     "<style>"+css+"</style>")
#         return html


    
    def score(self, objects, round_to=3, **param_dict):
        param_dict = self.prep_engine_params(param_dict)
#         nonce_val = param_dict.get("nonce", nonce_param.get_default())
#         redo = param_dict.get("redo", redo_param.get_default())
        
#         if redo and 9redo == "True"
        
        if param_dict["redo"] is False:
            return self.constant_scores.loc[objects.index]
        
        return pd.Series(np.random.random(len(objects)).round(round_to),
                         index=objects.index)
    
    
    def score_details(self, objects, round_to=3, **param_dict):
        param_dict = self.prep_engine_params(param_dict)
#         nonce_val = param_values.get("nonce", nonce_param.get_default())
#         redo = param_values.get("redo", redo_param.get_default())
        
        if param_dict["redo"] is False:
            return self.constant_score_details.loc[objects.index]
        
        descs = objects.Description.fillna("").str.split()
        choices = descs.apply(lambda ls: 
                              dict(zip(
                                  (np.random.choice(ls, size=2) 
                                   if (len(ls) > 2) else ls),
                                   np.random.rand(2).round(round_to)
                                                 ))
                             )
        return choices
    
    




