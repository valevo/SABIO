import numpy as np

class Engine:
    def __init__(self):
#         self.id  # str
#         self.name  # str
#         self.min_score  # float
#         self.params # list of EngineParam
        pass
    
class RandomEngine(Engine):
    def __init__(self, id_, params=None):
        super().__init__()
        self.name = "RandomEngine/v1.0"
        self.id = id_
        self.min_score = np.random.random()*100
        self.params = params
    
    def __lt__(self, other):
        if not isinstance(other, Dataset):
            raise ValueError
        return self.id < other.id
    
    def summary(self):
        return f"""
        <div>
            <h1> RandomEngine/v1.0 </h1>
            <p> Simple: assigns random scores to objects (as a percentage).</p>
            <p> min_score randomly chosen to be: {self.min_score}%.</p>
        </div>
        """
    
    def score(self, objects, with_details=True):
        detail_scores = None
        return np.random.random(len(objects))*100
    
#     def score_detail(self, object
    
    def __hash__(self):
        return hash(self.name)
    
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
                          
    
rand_engine = RandomEngine(id_=0, params=[nonce_param])