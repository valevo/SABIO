from tqdm import tqdm
tqdm.pandas()
import pandas as pd
import numpy as np

import joblib


from src.engines.Engine import CachedEngine
from src.engines.ngrams import Ngram

class PMIEngine(CachedEngine):
    def __init__(self, ID, name, params, cache_dir):
        super().__init__(ID, name, params, cache_dir)
        self.min_score = 0.
        self.max_score = 1.

        
    def _score_and_detail(self, dataset, round_to=3, **params):
        texts = dataset.segment(level="paragraph")
        self.pmi = PMI(texts)
        
        scores, details = self.typicality.process_objects(dataset.data.Texts)
        return scores, details

    
class PMI:
    def __init__(self, texts, **model_params):
        default_params = dict(ns=2, documents=texts, precompute_freqs=True)
        default_params.update(model_params)
        self.model = Ngram(**default_params)
        self.aggregate_func = np.mean
        
    def pmi(self, pair_str):
        w1, w2 = pair_str.split()
        return (
                self.model.prob(pair_str, log=True) - 
                (self.model.prob(w1, log=True) + 
                 self.model.prob(w2, log=True))
               )
    
    
    def process_object(self, row):
        pairs, pmis = [], []
        for text in row:
            cur_pairs = list(self.model.iter_ngrams(text, padding=False))
            pairs.extend(cur_pairs)
            pmis.extend(map(self.pmi, cur_pairs))
            
        return sorted(zip(pairs, pmis), key=lambda t:t[1]), self.aggregate_func(pmis)
    
    
    def norm(self, v, map_to_positive=True):
        if map_to_positive:
            v = v+np.min(v)
        return v/np.sum(v)
    
    

        
        
