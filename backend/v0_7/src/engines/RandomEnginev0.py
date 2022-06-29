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
        self.max_score = 1.
        
        # assign no longer necessary -> happens inside the functions
        # when redo=True
        self.constant_scores  = self.score(self.dataset.data, redo=True)
        self.constant_score_details = self.score_details(self.dataset.data, redo=True)
        

#     def score(self, objects, round_to=3, **param_dict):
#         param_dict = self.prep_engine_params(param_dict)
#         if param_dict["redo"] is False:
#             return self.constant_scores.loc[objects.index]

#         new_scores = pd.Series(np.random.random(len(objects)).round(round_to),
#                          index=objects.index)
#         new_scores.name = "score"
        
#         self.constant_scores = new_scores
#         return new_scores
    
    def score(self, objects, round_to=3, **param_dict):
        param_dict = self.prep_engine_params(param_dict)
        if param_dict["redo"] is False:
            return self.constant_scores.loc[objects.index]
        
        new_scores = np.random.random(len(self.dataset.data)).round(round_to)
        new_scores = pd.Series(new_scores, index=self.dataset.data.index, name="score")
        
        self.constant_scores = new_scores
        return new_scores.loc[objects.index]


    
#     def score_details(self, objects, round_to=3, **param_dict):
#         param_dict = self.prep_engine_params(param_dict)        
#         if param_dict["redo"] is False:
#             return self.constant_score_details.loc[objects.index]
        
        
#         # TODO: move this to Dataset -> make this the variable
#         # all engines & search algos work on
#         descs = objects.Description.fillna("").str.split()
        
#         new_choices = descs.apply(lambda ls: 
#                               dict(zip(
#                                   (np.random.choice(ls, size=2) 
#                                    if (len(ls) > 2) else ls),
#                                    np.random.rand(2).round(round_to)
#                                                  ))
#                              )
#         new_choices.name = "score_details"
#         self.constant_score_details = new_choices
#         return new_choices
    
    

    def score_details(self, objects, round_to=3, **param_dict):
        param_dict = self.prep_engine_params(param_dict)        
        if param_dict["redo"] is False:
            return self.constant_score_details.loc[objects.index]

        # TODO: move this to Dataset -> make this the variable
        # all engines & search algos work on
        # ----
        # TODO: include words in Title -> again, make this part of Dataset
        descs = self.dataset.data.Texts.str.split()
        
        
        def rand_choices(ls, n=2):
            words = np.random.choice(ls, size=min(2, len(ls)), replace=False)
            word_scores = np.random.random(len(words)).round(round_to)
            return dict(zip(words, word_scores))
        
        new_choices = descs.apply(rand_choices)
        new_choices.name = "score_details"
        
        self.constant_score_details = new_choices
        return new_choices.loc[objects.index]
        

    
    def score_and_detail(self, objects, round_to=3, **param_dict):
        scores = self.score(objects, round_to=round_to, **param_dict) 
        details = self.score_details(objects, round_to=round_to, **param_dict)
        return scores, details
    
    

#     def score(self, objects, round_to=3, **param_dict):
#         param_dict = self.prep_engine_params(param_dict)
# #         nonce_val = param_dict.get("nonce", nonce_param.get_default())
# #         redo = param_dict.get("redo", redo_param.get_default())
        
# #         if redo and 9redo == "True"
        
#         if param_dict["redo"] is False:
#             return self.constant_scores.loc[objects.index]
        
#         return pd.Series(np.random.random(len(objects)).round(round_to),
#                          index=objects.index)
    


#     def score_details(self, objects, round_to=3, **param_dict):
#         param_dict = self.prep_engine_params(param_dict)
# #         nonce_val = param_values.get("nonce", nonce_param.get_default())
# #         redo = param_values.get("redo", redo_param.get_default())
        
#         if param_dict["redo"] is False:
#             return self.constant_score_details.loc[objects.index]
        
#         descs = objects.Description.fillna("").str.split()
#         choices = descs.apply(lambda ls: 
#                               dict(zip(
#                                   (np.random.choice(ls, size=2) 
#                                    if (len(ls) > 2) else ls),
#                                    np.random.rand(2).round(round_to)
#                                                  ))
#                              )
#         return choices
