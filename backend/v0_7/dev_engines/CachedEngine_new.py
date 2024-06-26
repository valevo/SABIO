import logging


from tqdm import tqdm
tqdm.pandas()
import pandas as pd
import numpy as np

import joblib


from src.engines.engines import Engine
from src.engines.ngrams import Ngram



class CachedEngine(Engine):
    @classmethod
    def from_saved(cls, fname):
        self = joblib.load(fname)
        return self
    
    @classmethod
    def create_and_save(cls, dataset, id_, name, cached=True, param_list=[]):
        self = cls(dataset=dataset,
                   cached=cached,
                   id_=id_,
                   name=name,
                   params=param_list) #### <- change
        
        joblib.dump(self, self.id+".pkl")
        return self
    
    
    def __init__(self, cached=True, **engine_params):
        super().__init__(**engine_params)
        
        self.min_score = 0.
        self.max_score = 1.
        
        self.train_texts =  [p for t in self.dataset.data.Texts for p in t.split("\n")]
        
        self.cached = cached
        
#         self.engine = cls(texts, **cls_params)
        
#         if cached:
#             self.cached = False
#             self.scores_cached, self.details_cached = self.score_and_detail(self.dataset.data)
#             self.cached = True
#         else:
#             self.cached = False

    def cache(self):
        if self.cached:
            self.cached = False
            self.scores_cached, self.details_cached = self.score_and_detail(self.dataset.data)
            self.cached = True
        else:
            self.cached = False      


    def score(self, objects, round_to=3, **param_dict):
        raise NotImplementedError("CachedEngine only supports scoring & detailing together!") 

        
    def score_details(self, objects, round_to=3, **param_dict):
        raise NotImplementedError("CachedEngine only supports scoring & detailing together!") 
        
        
    def score_and_detail(self, objects, round_to=3, **param_dict):
        param_dict = self.prep_engine_params(param_dict)
        
        if self.cached:
            ids = objects.index
            return self.scores_cached.loc[ids], self.details_cached.loc[ids]
        
        object_scores, details = self.process_objects(objects.Texts)
        
        return object_scores, details

    
class Typicality(CachedEngine):
    def __init__(self, take_abs=False, model_params={}, **engine_params):
        super().__init__(**engine_params)
        
        default_params = dict(ns=3, documents=self.train_texts, precompute_freqs=True)
        default_params.update(model_params)
        self.model = Ngram(**default_params)
        
        # compute H
        self.H = self.cond_entropy(self.model, default_params["ns"])
        
        default_params.update(dict(ns=1))
        self.uni_model = Ngram(**default_params)
        self.uni_H = self.entropy(self.uni_model, 1)
        
        self.abs = abs if take_abs else self.identity
        self.normalise = self.percentile_norm
        
        self.cache()
  
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
    # = a2(a1(x))
    def normed_abs(self, x, q=100): return self.percentile_norm(self.absolute_value(x), q=q)
    
    # 1 - a3 = 1 - a2(a1(x))
    def inv_normed_abs(self, x, q=100):
        return 1 - self.normed_abs(x, q=q)
    
        # EMPIRICALLY FOUND NORMALISATION
    # -> advantage: can be applied directly, is dataset independent
#     def normalise(self, x):
#         return 1/(x + 1)
    

    @staticmethod
    def typical(entropy, log_prob):
        return entropy - (-log_prob)

    def _process_object(self, text):
        obj_prob = 0.
        l = 0
        for paragraph in text.split("\n"):
            grams = self.model.iter_ngrams(paragraph, as_tuples=True)
            for *rest, w in grams:
                w_prob = self.model.cond_prob(w, *rest, log=True)
                obj_prob += w_prob
                l += 1
                
                if not self.is_boundary_gram(" ".join((*rest, w))):
                    uni_prob = self.uni_model.prob(w, log=True)
                    yield w, self.typical(self.uni_H, uni_prob)

        obj_typ = self.typical(self.H, obj_prob/l)
        yield obj_typ
        
    def process_object(self, text):
        *gram_typicalities, obj_typicality = self._process_object(text)
        gram_typicalities = sorted(gram_typicalities, key=lambda t: t[1])
        return gram_typicalities, obj_typicality
    
    
    def process_objects(self, texts, round_to=2):
        tuples = texts.progress_apply(
#                        axis='columns', 
                        func=self.process_object
                )
        
        typs = tuples.apply(lambda t: t[1])
        typs = self.percentile_norm(typs, q=99.5).round(round_to)
        typs.name = "score"

        
        details = tuples.apply(lambda t: dict(t[0]))
        d = {k: v for smalld in tqdm(details, desc="constructing big d") for k, v in smalld.items()}
        
        values = np.asarray([d[k] for k in sorted(d.keys())]).round(round_to)
        values = self.inv_normed_abs(values, q=100)

        d = dict(zip(sorted(d.keys()), values))
        def swap_values(smalld):
            new_vals = sorted(((k, d[k]) for k in smalld), key=lambda t:t[1])
            top_unigrams = 5
            return dict(new_vals[-top_unigrams:])
        details = details.progress_apply(swap_values)
        details.name = "score_details"

        return typs, details
    
    
    
    

        
        
class PMI(CachedEngine):
    def __init__(self, take_abs=True, model_params={}, **engine_params):
        super().__init__(**engine_params)
        
        default_params = dict(ns=2, documents=self.train_texts, precompute_freqs=True)
        default_params.update(model_params)
        self.model = Ngram(**default_params)

        self.aggregate_func = np.mean
        self.abs = abs if take_abs else self.identity
        self.normalise = self.percentile_norm
        
        self.cache()

    @staticmethod
    def identity(x): return x
                    
    @staticmethod
    def percentile_norm(v, q=99.5):
        return (v - np.percentile(v, 100-q))/(np.percentile(v, q) - np.percentile(v, 100-q))

    def pmi(self, pair_str):
        w1, w2 = pair_str.split()
        return (
                self.model.prob(pair_str, log=True) - 
                (self.model.prob(w1, log=True) + 
                 self.model.prob(w2, log=True))
               )
        
    def process_object(self, text):
        pairs, pmis = []
        for paragraph in text.split("\n"):
            cur_pairs = list(self.model.iter_ngrams(paragraph, padding=False))
                
            pairs.extend(cur_pairs)
            pmis.extend(map(self.pmi, cur_pairs))
        
        pair_pmis = sorted(zip(pairs, pmis), key=lambda t:t[1])
        return pair_pmis, self.aggregate_func(pmis)

        
        
    def process_objects(self, texts, round_to=2):
        tuples = texts.progress_apply(self.process_object)
        
        aggr_pmis = tuples.apply(lambda t: t[1])
        aggr_pmis = self.normalise(aggr_pmis, q=99.5).round(round_to)
        aggr_pmis.name = "score"

        details = tuples.apply(lambda t: dict(t[0]))
        d = {k: v for smalld in tqdm(details, desc="constructing big d") for k, v in smalld.items()}
        
        values = np.asarray([d[k] for k in sorted(d.keys())]).round(round_to)
        values = self.normalise(values, q=100).round(round_to)

        d = dict(zip(sorted(d.keys()), values))
        def swap_values(smalld):
            new_vals = sorted(((k, d[k]) for k in smalld), key=lambda t:t[1])
            top_unigrams = 5
            return dict(new_vals[-top_unigrams:])
        details = details.progress_apply(swap_values)
        details.name = "score_details"

        return aggr_pmis, details
    
    
    
    
        
# default_params = dict(
#                     take_abs=True
# )
                  
# engine_params = dict(
#                     dataset=NMvW,
#                     id_="TypicalityEnginev0",
#                     name="TypicalityEngine/v0",
#                     params=[]
# )

    
    
# typE = CachedEngine(Typicality, default_params, cached=True, **engine_params)
                    
                  
# engine_params = dict(
#                     dataset=NMvW,
#                     id_="PMIEnginev0",
#                     name="PMIEngine/v0",
#                     params=[]
# )    

    
# pmiE = CachedEngine(PMI, default_params, cached=True, **engine_params)
            