import numpy as np

# from src.datasets import NMvW

class Engine:
    def __init__(self, id_, name, dataset, params):
        self.id = id_ # str
        self.name = name # str
        self.dataset = dataset # datasets.Dataset
        self.params = params # list of EngineParam
    

class RandomEngine(Engine):
    def __init__(self, **engine_args):
        super().__init__(**engine_args)
        self.min_score = 0. # np.random.random()*100
        self.params = params
        
#         self.scores = FILL TO MAKE SURE SCORES AREN'T RECOMPUTED

        self.constant_scores = self.score(self.dataset)
    
        self.constant_score_details = self.score_details(self.dataset)
    
    def description(self):
        return f"""
        <div>
            <h1> {self.name} (ID: {self.id}) </h1>
            <p> Simple: assigns random scores to objects (as a percentage).</p>
            <p> min_score randomly chosen to be: {self.min_score}%.</p>
        </div>
        """
    
    def score(self, objects, round_to=3, **param_values):       
        return np.random.random(len(objects)).round(round_to)
    
    
    def score_details(self, objects, round_to=3, **param_values):
        descs = objects.Description.fillna("").str.split()
        choices = descs.apply(lambda ls: 
                              dict(zip(
                                  (np.random.choice(ls, size=2) 
                                   if (len(ls) > 2) else ls),
                                   np.random.rand(2).round(round_to)
                                                 ))
                             )
        return choices
        
        
    def __hash__(self):
        return hash((self.__class__, self.id, self.name))
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "min_score": self.min_score,
            "params": [p.to_dict() for p in self.params]
        }
    

class EngineParam:
    def __init__(self, id_, label, description, control, default, options):
        self.id = id_
        self.label = label
        self.description = description
        
        if not control in {"select"}:
            raise ValueError("Control must be one of [select]!")
            
        self.control = control
        self.default = default
        self.options = options
        
        
    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "description": self.description,
            "control": self.control,
            "default": self.default,
            "options": self.options
        }
            

        
nonce_opts = {"useless1": "1", "useless2": "2"}        
nonce_param = EngineParam(id_=0, label="NonceParameter", 
                          description="does absolutely nothing",
                          control="select", default="useless1",
                          options=nonce_opts)

redo_param = EngineParam(id_=1, label="random rescore",
                         description="redo random scoring of dataset",
                         control="select", default="false",
                         options={"true": True, "false": False})

                          
# rand_engine = RandomEngine(id_="RandE_v0", 
#                            name="RandomEngine/v1.0",
#                            dataset=NMvW,
#                            params=[nonce_param])



class TypicalityEngine(Engine):
    def __init__(self, 