import numpy as np
import pandas as pd
from src.engines.Engine import Engine, EngineParam, CachedEngine



nonce_opts = {"1": "useless1", "2": "useless2"}    
nonce_vals = {k: k for k in nonce_opts}
nonce_param = EngineParam(ID="nonce", label="Nonce Parameter", 
                          description="This parameter has no effect and that is its point.",
                          control="select", default="1",
                          options=nonce_opts,
                         option2value=nonce_vals)

redo_opts = {"True": "yes", "False": "no"}
redo_vals = {"True": True, "False": False} 
redo_param = EngineParam(ID="redo", label="Rescore Parameter",
                         description="Redo the random scoring of the dataset.",
                         control="select", default="False",
                         options=redo_opts,
                        option2value=redo_vals)



class RandomEngine(CachedEngine):
    def __init__(self, ID, name, params, cache_dir):
        super().__init__(ID, name, params, cache_dir)
        self.min_score = 0.
        self.max_score = 1.

    
    def is_cached(self, dataset, **params):
#         params = self.prep_engine_params(params)
        print(f"{self.ID} CHECKING IF CACHED")
        print(f"{self.ID} GOT PARAMS {params}")
        if params["redo"] is True:
            print(f"{self.ID} ")
            return False  # trigger recomputation of scores
        return super().is_cached(dataset, **params)
    
        
    def _score_and_detail(self, dataset, round_to=3, **params):
        print(f"{self.ID} RESCORING")
#         params = self.prep_engine_params(params)
        
        scores = np.random.random(len(dataset)).round(round_to)
        scores = pd.Series(scores, index=dataset.index, name="score")
        
        words = dataset.tokenise()
        def rand_choices(ls, n=2):
            words = np.random.choice(ls, size=min(2, len(ls)), replace=False)
            word_scores = np.random.random(len(words)).round(round_to)
            return dict(zip(words, word_scores))
        
        word_choices = words.apply(rand_choices)
        word_choices.name = "score_details"
        return scores, word_choices


                                  
                                  
                                  
    