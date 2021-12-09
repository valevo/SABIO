import numpy as np

# from src.datasets import NMvW


class Engine:
    def __init__(self, id_, name, dataset, params):
        self.id = id_ # str
        self.name = name # str
        self.dataset = dataset # datasets.Dataset
        self.params = params # list of EngineParam
    
    def description(self):
        with open(self.id+".html") as handle:
            html = handle.read()
        with open("descriptions.css") as handle:
            css = handle.read()
        
        html.replace("<style></style>",
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