import numpy as np

import joblib


### TODO ###
############
# - selecting "Title" & "Description" columns should be done by Dataset (as something like Dataset.get_scoring_data())
# - 


class PMIEngine(CachedEngine):
    @classmethod
    def from_saved(cls, fname="PMIEnginev0.pkl"):
        return super().from_saved(fname)
    
    @classmethod
    def create_and_save(cls, dataset, cached=True, **engine_params):
        return super().create_and_save(
            dataset, "PMIEnginev0", "PMIEngine/v0", cached=True, **engine_params
        )  
    
    def __init__(self, cls_params, cached=True, **engine_params):
        super().__init__(PMI, cls_params, cached=cached, **engine_params)



class TypicalityEngine(CachedEngine):
    @classmethod
    def from_saved(cls, fname="TypicalityEnginev0.pkl"):
        return super().from_saved(fname)
    
    @classmethod
    def create_and_save(cls, dataset, cached=True, **engine_params):
        return super().create_and_save(
            dataset, "TypicalityEnginev0", "TypicalityEngine/v0", cached=True, **engine_params
        )
    
    def __init__(self, cls_params, cached=True, **engine_params):
        super().__init__(Typicality, cls_params, cached=cached, **engine_params)




class CachedEngine(Engine):
    @classmethod
    def from_saved(cls, fname):
        self = joblib.load(fname)
        return self
    
    @classmethod
    def create_and_save(cls, dataset, id_, name, cached=True, **engine_params):
        
        self = cls(dataset=dataset,
                   cached=cached,
                    id_=id_,
                    name=name,
                    params=[]) #### <- change
        
        joblib.dump(self, self.id+".pkl")
        return self
    
    
    def __init__(self, cls, cls_params, cached=True, **engine_params):
        super().__init__(**engine_params)
        self.min_score = 0. #### change
        
        text_data = self.dataset.data[["Title", "Description"]].fillna("")
                
        self.engine = cls(text_data.values.flatten(), **cls_params) #### class & params
        
        if cached:
            cached = False
            self.scores_cached, self.details_cached = self.score_and_detail(text_data)
            
            self.cached = True
        else:
            self.cached = False
            
            
    def score(self, objects, round_to=3, **param_dict):
        raise NotImplementedError("CachedEngine only supports scoring & detailing together!") 

        
    def score_details(self, objects, round_to=3, **param_dict):
        raise NotImplementedError(f"{self.id} only supports scoring & detailing together!") 
        
        
        
    def score_and_detail(self, objects, round_to=3, **param_dict):
        param_dict = self.prep_engine_params(param_dict)
        
        if self.cached:
            ids = objects.index
            return self.typs_cached.loc[ids], self.details_cached.loc[ids]
        
        object_scores, details = self.engine.process_ojects(
                            objects[["Title", "Description"]]
        )
        
        return object_scores, details
