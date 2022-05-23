import numpy as np

import joblib

class PMI:
    def __init__(self, texts, **model_params):
        default_params = dict(ns=2, documents=texts, precompute_freqs=True)
        default_params.update(model_params)
        self.model = Ngram(**default_params)
        
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
            
        return sorted(zip(pairs, pmis), key=lambda t:t[1]), np.mean(pmis)
    
    
    # distribution at q=99.5 is very narrow
    # -> q=95 is broader and retains 90% of objects
    @staticmethod
    def percentile_norm(v, q=95):
        return (v - np.percentile(v, 100-q))/(np.percentile(v, q) - np.percentile(v, 100-q))

    # taking sqrt implies scores centered & symmetric around 0.5
    # (otherwise high skew towards 0)
    def norm(self, v, q=95, do_sqrt=False):
        normed = self.percentile_norm(v, q)
        return normed**0.5 if do_sqrt else normed
        
    def process_objects(self, rows):
        tuples = rows.progress_apply(
                    axis='columns', 
                    func=self.process_object
                )
        
        scores = tuples.apply(lambda t: t[1])
        scores = self.norm(scores, do_sqrt=True)
        scores.name = "scores"
        
        
        details = tuples.apply(lambda t: t[0])
        all_vals = np.asarray([v for obj_details in details for pair, v in obj_details])
        val_dict = dict(zip(all_vals, self.norm(all_vals)))
        def swap_values(pair_ls, keep_top=2):
            return sorted([(w, val_dict[v]) for w, v in pair_ls],
                          key=lambda t: t[1],
                          reverse=True)[:keep_top]
        details.apply(swap_values)
        details.name = "score details"
        return scores, details

    
    
    


class PMIEngine(Engine):
    @classmethod
    def from_saved(cls, fname="PMIEnginev0.pkl"):
        self = joblib.load(fname)
        return self
    
    @classmethod
    def create_and_save(cls, dataset, cached=True, **engine_params):
        
        self = cls(dataset=dataset,
                   cached=cached,
                    id_="PMIEnginev0", ####
                    name="PMIEngine/v0", ####
                    params=[]) #### <- change
        
        joblib.dump(self, self.id+".pkl")
        return self
    
    
    def __init__(self, cached=True, **engine_params):
        super().__init__(**engine_params)
        self.min_score = 0.
        
        texts = self.dataset.data[["Title", "Description"]].fillna("").values.flatten()
        
        self.pmi = PMI(texts) #### class & params
        
        
        if cached:
            cached = False
            self.scores_cached, self.details_cached = self.score_and_detail(
                                self.dataset.data[["Title", "Description"]].fillna("")
            )
            
            self.cached = True
        else:
            self.cached = False
            
            
    def score(self, objects, round_to=3, **param_dict):
        raise NotImplementedError("PMIEngine only supports scoring & detailing together!") 

        
    def score_details(self, objects, round_to=3, **param_dict):
        raise NotImplementedError("PMIEngine only supports scoring & detailing together!") 
        
        
        
    def score_and_detail(self, objects, round_to=3, **param_dict):
        param_dict = self.prep_engine_params(param_dict)
        
        if self.cached:
            ids = objects.index
            return self.typs_cached.loc[ids], self.details_cached.loc[ids]
        
        object_scores, details = self.pmi.process_ojects(  #### reference to actual engine
                            objects[["Title", "Description"]]
        )
        
        return object_scores, details

            
            
            