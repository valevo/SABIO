import logging


from tqdm import tqdm
tqdm.pandas()
import pandas as pd
import numpy as np

import joblib


from src.engines.engines import Engine
from src.engines.ngrams import Ngram


class Typicality:
    def __init__(self, texts, take_abs=False, **model_params):
        default_params = dict(ns=3, documents=texts, precompute_freqs=True)
        default_params.update(model_params)
        self.model = Ngram(**default_params)
        
        # compute H
        self.H = self.cond_entropy(self.model, default_params["ns"])
        
        default_params.update(dict(ns=1))
        self.uni_model = Ngram(**default_params)
        self.uni_H = self.entropy(self.uni_model, 1)
        
        self.abs = abs if take_abs else self.identity
        self.normalise = self.percentile_norm
  
    @staticmethod
    def is_boundary_gram(gram):
        return (gram.find("<s>") >= 0) or (gram.find("</s>") >= 0)
        
        
    def entropy(self, model, n):
        probs = [model.prob(*gram.split(" ")) for gram in tqdm(model.vocab(n))]
        arr = np.asarray(probs)
        return -np.sum(arr*np.log2(arr))
    
    
    def cond_entropy(self, model, n):
        H_context = self.entropy(model, n-1)
        H_joint = self.entropy(model, n)
        return H_joint - H_context

                
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
    def normed_abs(self, x, q=100): return self.percentile_norm(self.absolute_value(x), q=q)
    
    # 1 - a3
    def inv_normed_abs(self, x, q=100):
        return 1 - self.normed_abs(x, q=q)
    

    @staticmethod
    def typical(entropy, log_prob):
        return entropy - (-log_prob)

    def _process_object(self, row):
        obj_prob = 0.
        l = 0
        for text in row:
            grams = self.model.iter_ngrams(text, as_tuples=True)
            for *rest, w in grams:
                w_prob = self.model.cond_prob(w, *rest, log=True)
                obj_prob += w_prob
                l += 1
                
                if not self.is_boundary_gram(" ".join((*rest, w))):
                    uni_prob = self.uni_model.prob(w, log=True)
                    yield w, self.typical(self.uni_H, uni_prob)

        obj_typ = self.typical(self.H, obj_prob/l)
        yield obj_typ
        
    def process_object(self, row):
        *gram_typicalities, obj_typicality = self._process_object(row)
        gram_typicalities = sorted(gram_typicalities, key=lambda t: t[1])
        return gram_typicalities, obj_typicality
    
    
    def process_objects(self, rows):
        tuples = rows.progress_apply(
                        axis='columns', 
                        func=self.process_object
                )
        
        typs = tuples.apply(lambda t: t[1])
        typs = self.percentile_norm(typs, q=99.5)
        typs.name = "score"

        
        
        details = tuples.apply(lambda t: dict(t[0]))
        d = {k: v for smalld in tqdm(details, desc="constructing big d") for k, v in smalld.items()}
        
        values = np.asarray([d[k] for k in sorted(d.keys())])
        values = self.inv_normed_abs(values, q=100)

        d = dict(zip(sorted(d.keys()), values))
        def swap_values(smalld):
            new_vals = sorted(((k, d[k]) for k in smalld), key=lambda t:t[1])
            return dict(new_vals[-2:])
        details = details.progress_apply(swap_values)
        details.name = "score_details"

        return typs, details

    

    

class TypicalityEngine(Engine):
    @classmethod
    def from_saved(cls, fname="TypicalityEnginev0.pkl"):
        self = joblib.load(fname)
        return self
    
    @classmethod
    def create_and_save(cls, dataset, cached=True, **engine_params):
        
        self = cls(dataset=dataset,
                   cached=cached,
                    id_="TypicalityEnginev0",
                    name="TypicalityEngine/v0",
                    params=[])
        
        joblib.dump(self, self.id+".pkl")
        return self
    
    def __init__(self, cached=True, **engine_params):
        super().__init__(**engine_params)
        self.min_score = 0.

        
        texts = self.dataset.data[["Title", "Description"]].fillna("").values.flatten()

        self.typicality = Typicality(texts, take_abs=False)
            
        
        if cached:
            self.cached = False
            self.typs_cached, self.details_cached = self.score_and_detail(
                            self.dataset.data[["Title", "Description"]].fillna("")
            )
            self.cached = True
        else:
            self.cached = False

    
    
    def score(self, objects, round_to=3, **param_dict):
        raise NotImplementedError("TypicalityEngine only supports scoring & detailing together!") 

        
    def score_details(self, objects, round_to=3, **param_dict):
        raise NotImplementedError("TypicalityEngine only supports scoring & detailing together!") 
        
        
    def score_and_detail(self, objects, round_to=3, **param_dict):
        param_dict = self.prep_engine_params(param_dict)
        
        if self.cached:
            ids = objects.index
            return self.typs_cached.loc[ids], self.details_cached.loc[ids]
            
            
        object_typicalities, details = self.typicality.process_objects(
                                                        objects[["Title", "Description"]])
        
        return object_typicalities, details
        
#         tuples = objects[["Title", "Description"]].progress_apply(
#                                                     axis='columns', 
#                                                     func=self.typicality.process_object
#                                                     )
        
#         obj_typs = tuples.apply(lambda t: t[1])
#         obj_typs = self.typicality.normalise(obj_typs)
#         obj_typs.name = "score"
        
#         only_last = 2
#         details = tuples.apply(lambda t: dict(t[0])) #[:only_last]))
        
#         d = {k: v for smalld in tqdm(details, desc="constructing big d") for k, v in smalld.items()}
        
#         values = 1 - self.typicality.normalise(
#                                                abs(
#                                                    np.asarray([d[k] for k in sorted(d.keys())] )
#                                                ), 
#                                                q=100
#                                                )
    
#         d = dict(zip(sorted(d.keys()), values))  
#         details = details.progress_apply(lambda smalld: {k: d[k] for k in smalld})
#         details.name = "score_details"
        
#         return obj_typs, details
