import os
import pandas as pd
import csv

class Engine:
    def __init__(self, ID, name, params):
        self.ID = ID
        self.name = name
        self.params = params
        
    def prep_engine_params(self, param_dict):
        return {p.ID: p.get(param_dict.get(p.ID, p.default_value)) for p in self.params}

    def description(self):
        # was src/engines/{self.ID}.html
        with open(f"./engines/{self.ID}.html") as handle:
            html = handle.read()
            
        with open("./engines/descriptions.css") as handle:
            css = handle.read()
        
        html = html.replace("<style></style>",
                    "<style>"+css+"</style>")
        return html
    
    def __hash__(self):
        return hash((self.__class__, self.ID, self.name))

    def to_dict(self):
        return {
            "id": self.ID,
            "name": self.name,
            "min_score": self.min_score,
            "params": [p.to_dict() for p in self.params]
        }

    @staticmethod
    def identity(x): return x

    # a1
    @staticmethod
    def absolute_value(x): return abs(x)
    
    # a2
    # q=99.5 (empirically) leads to 1% of the data being outside the range
    @staticmethod
    def percentile_norm(v, q=99.5):
        return (v - np.percentile(v, 100-q))/(np.percentile(v, q) - np.percentile(v, 100-q))

    # a3
    # = a2(a1(x))
    def normed_abs(self, x, q=100): return self.percentile_norm(self.absolute_value(x), q=q)
    
    # 1 - a3 = 1 - a2(a1(x))
    def inv_normed_abs(self, x, q=100):
        return 1 - self.normed_abs(x, q=q)

    
class CachedEngine(Engine):
    def __init__(self, ID, name, params, cache_dir):
        super().__init__(ID, name, params)
        self.cache_dir = cache_dir

    def get_cached_filename(self, dataset):
        filename = f"{self.ID}_{dataset.ID}.csv.gz"
        return os.path.join(self.cache_dir, filename)
        
    def is_cached(self, dataset, **params):
        return os.path.isfile(self.get_cached_filename(dataset))
    
    def load_scores_for(self, dataset, **params):
        loaded = pd.read_csv(self.get_cached_filename(dataset))
        loaded = loaded.set_index("ID")
        return loaded.score, loaded.score_details.apply(eval)
    
    
    def save_scores_for(self, scores, details, dataset, **params):
        df = pd.concat([scores, details], axis=1)
        df = df.set_index(scores.index)
        df.columns = ["score", "score_details"]
        
        filename = self.get_cached_filename(dataset)
        df.to_csv(filename, compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1})
        
    
    def _score_and_detail(self, dataset, indices, **params):
        raise NotImplementedError("To be implemented by an actual engine!")
    
    
    def score_and_detail(self, dataset, indices, **params):
        params = self.prep_engine_params(params)
        if self.is_cached(dataset, **params):
            loaded_scores, loaded_details = self.load_scores_for(dataset, **params)
            return loaded_scores.loc[indices], loaded_details.loc[indices]
                
        scores, details = self._score_and_detail(dataset, indices, **params)
        
        self.save_scores_for(scores, details, dataset, **params)
        
        return scores.loc[indices], details.loc[indices]
        

class EngineParam:
    def __init__(self, ID, label, description, control, default, options, option2value):
        self.ID = ID
        self.label = label
        self.description = description
        
        if not control in {"select"}:
            raise ValueError("Control must be one of [select]!")
            
        self.control = control
        self.default = default
        self.options = options
        self.option2value = option2value
        self.default_value = self.option2value[self.default]

    def get(self, key):
        return self.option2value.get(key, self.default_value)

    
    def to_dict(self):
        return {
            "id": self.ID,
            "label": self.label,
            "description": self.description,
            "control": self.control,
            "default": self.default,
            "options": self.options
        }
    
    
    
