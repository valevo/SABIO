import numpy as np
import pandas as pd

from src.engines.engines import Engine, EngineParam

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
        
    
    def score(self, objects, round_to=3, **param_values):
        nonce_val = param_values["nonce"]
        redo = param_values.get("redo", False)
        
        if not redo:
            return self.constant_scores.loc[objects.index]
        
        return pd.Series(np.random.random(len(objects)).round(round_to),
                         index=self.dataset.data.index)
    
    
    def score_details(self, objects, round_to=3, **param_values):
        nonce_val = param_values["nonce"]
        redo = param_values.get("redo", False)
        
        if not redo:
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
    
    


nonce_opts = {"useless1": "1", "useless2": "2"}        
nonce_param = EngineParam(id_="nonce", label="NonceParameter", 
                          description="does absolutely nothing",
                          control="select", default="useless1",
                          options=nonce_opts)

redo_opts = {"true": True, "false": False}
redo_param = EngineParam(id_="redo", label="random rescore",
                         description="redo random scoring of dataset",
                         control="select", default="false",
                         options=redo_opts)


