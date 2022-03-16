import numpy as np
import pandas as pd

from src.engines.engines import Engine, EngineParam


class VocabularyEngine(Engine):
    def __init__(self, **engine_args):
        super().__init__(**engine_args)
        self.min_score = 0. # np.random.random()*100
        self.max_score = 1.
        self.vocab_parser = re.compile("\s*,\s*")

        # constanct scores and details make no sense for this engine!
#         self.constant_scores  = self.score(self.dataset.data)
#         self.constant_score_details = self.score_details(self.dataset.data)
        

    # assumes that `raw_vocab` is a string of comma-separated terms
    def vocab2re(self, raw_vocab):
        v_ls = self.vocab_parser.split(raw_vocab.strip())
        return re.compile("|".join(v_ls))
        
        
    def score(self, objects, round_to=3, **param_dict):
        vocab_re = self.vocab2re(param_dict["vocabulary"])
        
        scores = objects[["Title", "Description"]].apply(
            lambda r: len([w for txt in row
                          for w in vocab_re.findall(txt)])
        )
        
        scores.name = "score"
        
        return scores
    
    
    def score_details(self, objects, round_to=3, **param_dict):
        raise NotImplementedError("VocabularyEngine doesn't support details without scoring!")
        
        
    def score_and_detail(self, objects, round_to=3, **param_dict):
        vocab_re = self.vocab2re(param_dict["vocabulary"])
        
        from collections import Counter 
        def process_obj(o):
            counts = Counter([w for txt in row for w in vocab_re.findall(txt)])
            score = sum(counts.values())
            percents = {w: (c/score) for w, c in counts.items()}
            
            return percents, score
        
        tups = objects.apply(process_obj)
        
        scores = tups.apply(lambda t: t[1])
        scores = scores/scores.max()
        scores.name = "score"
        
        details = tups.apply(lambda t: t[0])
        details.name = "score_details"
        
        return scores, details
        
        
        
    
            
                
                
            

