from tqdm import tqdm
tqdm.pandas()
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from ngrams import Ngram


class Typicality:
    def __init__(self, texts, take_abs=True, **model_params):
        default_params = dict(ns=3, documents=texts, precompute_freqs=True)
        default_params.update(model_params)
        self.model = Ngram(**default_params)
        
        # compute H
        self.H = self.cond_entropy(self.model, default_params["ns"])
        
        default_params.update(dict(ns=1))
        self.uni_model = Ngram(**default_params)
        self.uni_H = self.entropy(self.uni_model, 1)
        
        self.abs = (lambda x: abs(x)) if take_abs else (lambda x: x)
        self.normalise = lambda x: x
                
        
#         self.dataset_max = None
#         self.obj_typicalities = None
#         self.gram_typicalities = None


    # EMPIRICALLY FOUND NORMALISATION
    # -> advantage: can be applied directly, is dataset independent
#     def normalise(self, x):
#         return 1/(x + 1)
        

    def typical(self, entropy, log_prob):
        return self.normalise(self.abs(entropy - (-log_prob)))
    
    
    @staticmethod
    def is_boundary_gram(gram):
        return (gram.find("<s>") >= 0) or (gram.find("</s>") >= 0)
        
        
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
#                     yield w, self.normalise(self.abs(self.uni_H - (-uni_prob)))
                

#                 if not self.is_boundary_gram(" ".join((*rest, w))):
#                     yield (*rest, w), self.normalise(abs(self.H - (-w_prob)))

        obj_typ = self.typical(self.H, obj_prob/l)
#         obj_typ = self.normalise(
#                         self.abs(self.H - (-obj_prob/l))
#                   )

        yield obj_typ
        
    def process_object(self, row):
        *gram_typicalities, obj_typicality = self._process_object(row)
        gram_typicalities = sorted(gram_typicalities, key=lambda t: t[1])
        return gram_typicalities, obj_typicality
        
        
    def entropy(self, model, n):
        probs = [model.prob(*gram.split(" ")) for gram in tqdm(model.vocab(n))]
        arr = np.asarray(probs)
        return -np.sum(arr*np.log2(arr))
    
    
    def cond_entropy(self, model, n):
        H_context = self.entropy(model, n-1)
        H_joint = self.entropy(model, n)
        return H_joint - H_context



# class TypicalityEngine(Engine):
#     def __init__(self, **engine_params):
#         super().__init__(**engine_args)
#         self.min_score = 0. # np.random.random()*100

#         texts = self.dataset.data.apply(lambda r: 
#                                         r["Title"] + r["Description"], axis="columns")
#         self.typicality = Typicality(texts)
        
        
        
#         a(o) = |H(P) - [- 1/|o|*log(P(o))]|
#         a(o) > 0
        
#         a(o) < inf 
#         -> practically: a(o) < a(o') w. o' minimises P(o') 
#         => could use to change a: O -> [0, inf) into a': O -> [0, 1]


    
    
#     def score(self, objects, round_to=3, **param_dict):
#         raise NotImplementedError("TypicalityEngine only supports scoring & detailing together!") 

#     def score_details(self, objects, round_to=3, **param_dict):
#         raise NotImplementedError("TypicalityEngine only supports scoring & detailing together!") 
        
#     def score_and_detail(self, objects, round_to=3, **param_dict):
#         param_dict = self.prep_engine_params(param_dict)
        
#         tuples = objects[["Title", "Description"]].progress_apply(axis='columns', 
#                                                          func=lambda r: typ_E.process_object(r))
        
#         obj_typs = tuples.apply(lambda t: t[1])
        
#         only_last = 2
#         details = tuples.apply(lambda t: dict(t[0]))
        
#         return obj_typs, details
 