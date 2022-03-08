import numpy as np

# from src.datasets import NMvW


class Engine:
    def __init__(self, id_, name, dataset, params):
        self.id = id_ # str
        self.name = name # str
        self.dataset = dataset # datasets.Dataset
        self.params = params # list of EngineParam
        
    def prep_engine_params(self, param_dict):
        return {p.id: param_dict.get(p.id, p.default_value) for p in self.params}
#         return {p.id: p.get() for p, v in self.params}

    
    def description(self):
        with open(f"src/engines/{self.id}.html") as handle:
            html = handle.read()
            
        with open("src/engines/descriptions.css") as handle:
            css = handle.read()
        
        html = html.replace("<style></style>",
                    "<style>"+css+"</style>")
        return html
    
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
    def __init__(self, id_, label, description, control, default, options, option2value):
        self.id = id_
        self.label = label
        self.description = description
        
        if not control in {"select"}:
            raise ValueError("Control must be one of [select]!")
            
        self.control = control
        self.default = default
        self.options = options
        self.option2value = option2value
        self.default_value = self.option2value[self.default]
        
#     def get_default(self):
#         return self.options[self.default]
    
#     def get_default_value(self):
#         return self.option2value[self.default]
    
    def get(self, key):
        return self.option2value.get(key, self.default_value)
        
        
    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "description": self.description,
            "control": self.control,
            "default": self.default,
            "options": self.options
        }